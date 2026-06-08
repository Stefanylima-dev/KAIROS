from flask import Flask, render_template, request, jsonify 
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def menu():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    
    hoje = datetime.now().date()
    
    
    cursor.execute("SELECT * FROM produtos WHERE data_validade <= %s AND quantidade > 0", (hoje,))
    produtos_vencidos = cursor.fetchall()
    
    for produto in produtos_vencidos:
    
        p_custo = float(produto['preco']) if produto['preco'] else 0.0
        prejuizo_calculado = int(produto['quantidade']) * p_custo
        
        try:
            comando_perda = """
                INSERT INTO perdas (nome_produt, quantidade, lote, data_validade, motivo, preco_custo, prejuizo) 
                VALUES (%s, %s, %s, %s, 'Vencimento', %s, %s)
            """
            valores_perda = (
                produto['nome'], 
                produto['quantidade'], 
                produto['lote'], 
                produto['data_validade'],
                p_custo,
                prejuizo_calculado
            )
            cursor.execute(comando_perda, valores_perda)
            
          
            cursor.execute("DELETE FROM produtos WHERE id = %s", (produto['id'],))
            
        except mysql.connector.Error as erro_sql:
            print(f"\n❌ ERRO NO BANCO AO MOVER {produto['nome']}: {erro_sql}\n")
            conexao.rollback()

    conexao.commit()
    
 
    limite_alerta = hoje + timedelta(days=30)
    
    comando_alertas = """
        SELECT id, nome, quantidade, lote, data_validade 
        FROM produtos 
        WHERE data_validade <= %s AND quantidade > 0
        ORDER BY data_validade ASC
    """
    cursor.execute(comando_alertas, (limite_alerta,))
    produtos_criticos = cursor.fetchall()
    
    for produto in produtos_criticos:
        if isinstance(produto['data_validade'], str):
            data_prod = datetime.strptime(produto['data_validade'], "%Y-%m-%d").date()
        else:
            data_prod = produto['data_validade']
            
        produto['status_validade'] = 'alerta'
        produto['dias_restantes'] = (data_prod - hoje).days

    cursor.close()
    conexao.close()
    
    return render_template('menu.html', alertas=produtos_criticos)
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')


def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",      
        password="1234",    
        database="sistema_estoqu"
    )

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('name_product')
    codigo_barras = request.form.get('codigo_barras')
    quantidade = request.form.get('amount_product')
    lote = request.form.get('batch_product')
    preco = request.form.get('preco')
    preco_venda = request.form.get('preco_venda')
    data_validade = request.form.get('date_maturity')
   
   

    conexao = get_db_connection()
    cursor = conexao.cursor()

    comando = "INSERT INTO produtos (nome,codigo_barras, quantidade, lote, preco, preco_venda, data_validade ) VALUES (%s, %s, %s, %s, %s,%s,%s)"
    valores = (nome, codigo_barras, quantidade, lote, preco, preco_venda, data_validade)

    cursor.execute(comando, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return "Produto cadastrado no banco com sucesso!"


def alerta(data_validade):
    if isinstance(data_validade, str):
        data_vencimento_c = datetime.strptime(data_validade, '%Y-%m-%d').date()
    else:
        data_vencimento_c = data_validade 
    
    data_atual = datetime.now().date()
    diferenca_dias = (data_vencimento_c - data_atual).days

    if diferenca_dias <= 0:
        return "Produto vencido"
    elif diferenca_dias <= 30:
        return f"Produto vence em {diferenca_dias} dias"
    else:
        return "No prazo"
    

@app.route('/estoque')
def percorrer_estoque():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True) 
    
    cursor.execute("SELECT * FROM produtos")
    lista_produtos = cursor.fetchall()

    for produto in lista_produtos:
        resultado_alerta = alerta(produto['data_validade'])
        produto['alerta'] = resultado_alerta

    cursor.close()
    conexao.close()
   
    return render_template('estoque.html', produtos=lista_produtos)


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    produtos_encontrados = []
    termo_busca = ""
    
    if request.method == 'POST':
        termo_busca = request.form.get('termo_busca', '').strip()
        
        if termo_busca:
            conexao = get_db_connection()
            cursor = conexao.cursor(dictionary=True)
            
            comando = "SELECT * FROM produtos WHERE nome LIKE %s"
            cursor.execute(comando, (f"%{termo_busca}%",))
            produtos_encontrados = cursor.fetchall()
            
            for produto in produtos_encontrados:
                produto['alerta'] = alerta(produto['data_validade'])
                
            cursor.close()
            conexao.close()

    return render_template('buscar.html', produtos=produtos_encontrados, termo=termo_busca)


@app.route('/relatorio_geral')
def relatorio_vendas():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM vendas ORDER BY data_venda DESC")
    lista_vendas = cursor.fetchall()
    
    cursor.execute("SELECT * FROM perdas ORDER BY data_perda DESC")
    lista_perdas = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return render_template('vendas.html', vendas=lista_vendas, perdas=lista_perdas)

@app.route('/registrar_venda/<int:id>', methods=['POST'])
def registrar_venda(id):
    qtd_vendida = int(request.form.get('qtd_desejada', 1))

    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (id,))
    produto = cursor.fetchone()
    
    if produto:
        nova_quantidade = int(produto['quantidade']) - qtd_vendida
        if nova_quantidade == 0 :
            cursor.execute("DELETE FROM produtos WHERE id = %s", (id,))
        if nova_quantidade >= 0:
            cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (nova_quantidade, id))
        

            p_custo = float(produto['preco']) if produto['preco'] else 0.0
            p_venda = float(produto['preco_venda']) if produto['preco_venda'] else 0.0
 
            faturamento_bruto = qtd_vendida * p_venda
            lucro_total = qtd_vendida * (p_venda - p_custo)

            comando_venda = """
                INSERT INTO vendas (nome_produto, quantidade, lote, preco_venda, faturamento_bruto, lucro) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores_venda = (produto['nome'], qtd_vendida, produto['lote'], p_venda, faturamento_bruto, lucro_total)
            cursor.execute(comando_venda, valores_venda)
            
            conexao.commit()
            mensagem = f"Venda de {qtd_vendida} unidade(s) realizada com sucesso! 💰"
        else:
            mensagem = f"Erro: Estoque insuficiente! Você tentou vender {qtd_vendida} un, mas só existem {produto['quantidade']} un. ⚠️"
    else:
        mensagem = "Produto não encontrado! ❌"
   

    cursor.close()
    conexao.close()
    return f"<h3>{mensagem}</h3><br><a href='/estoque'>Voltar ao Estoque</a>"

@app.route('/relatorio_perdas')
def relatorio_perdas():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM perdas ORDER BY data_perda DESC")
    lista_perdas = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return render_template('perdas.html', perdas=lista_perdas)

@app.route('/processar_vencidos', methods=['POST'])
def processar_vencidos():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    hoje = datetime.now().date()

    cursor.execute("SELECT * FROM produtos WHERE data_validade <= %s AND quantidade > 0", (hoje,))
    produtos_vencidos = cursor.fetchall()
    
    contador_perdas = 0
    
    for produto in produtos_vencidos:
        comando_perda = """
            INSERT INTO perdas (nome_produt, quantidade, lote, data_validade, motivo) 
            VALUES (%s, %s, %s, %s, 'Vencimento')
        """
        valores_perda = (produto['nome'], produto['quantidade'], produto['lote'], produto['data_validade'])
        cursor.execute(comando_perda, valores_perda)

        cursor.execute("DELETE FROM produtos WHERE id = %s", (produto['id'],))
        
        contador_perdas += 1
        
    conexao.commit()
    cursor.close()
    conexao.close()
    
    if contador_perdas > 0:
        mensagem = f"Sucesso! {contador_perdas} produto(s) vencido(s) foram movidos para o relatório de perdas. ⚠️"
    else:
        mensagem = "Ótima notícia! Nenhum produto vencido foi encontrado no estoque hoje. 🎉"
        
    return f"<h3>{mensagem}</h3><br><a href='/estoque'>Voltar ao Estoque</a> | <a href='/relatorio_perdas'>Ver Perdas</a>"

@app.route('/buscar_por_codigo', methods=['POST'])
def buscar_por_codigo():
    dados = request.get_json()
    codigo_lido = dados.get('codigo')
    
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM produtos WHERE codigo_barras = %s", (codigo_lido,))
    produto = cursor.fetchone()
    
    cursor.close()
    conexao.close()
    
    if produto:
        status_alerta = alerta(produto['data_validade'])
        
        return jsonify({
            "status": "encontrado",
            "id": produto['id'],
            "nome": produto['nome'],
            "quantidade": produto['quantidade'],
            "lote": produto['lote'],
            "alerta": status_alerta
        })
    else:
        return jsonify({
            "status": "nao_encontrado",
            "codigo": codigo_lido
        })

if __name__ == '__main__':
    app.run(debug=True, port=8080)