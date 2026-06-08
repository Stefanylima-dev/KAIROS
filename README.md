# 🚀 Kairós - Sistema Inteligente de Gestão de Estoque e Validade

O **Kairós** é uma aplicação web desenvolvida para resolver um desafio real enfrentado por muitos comércios: a gestão inteligente de estoque com foco no controle rigoroso de prazos de validade. Integrando **Python (Flask)** e **MySQL**, o sistema automatiza processos críticos para minimizar perdas financeiras e combater o desperdício de alimentos.

---

## 📸 Demonstração do Sistema

<div align="center">
  
  <img src="Menu.png" alt="Painel de Controle Kairós" width="85%"><br>
  <p><strong>📊 Painel de Controle com alertas automáticos</strong></p>
  
  <img src="Tela_de_Cadastro.png" alt="Cadastro de Produtos" width="85%"><br>
  <p><strong>📥 Tela de Inserção e Cadastro Inteligente</strong></p>

  <img src="Tela_de_Busca.png" alt="Busca de Produtos" width="85%"><br>
  <p><strong>🔍 Sistema de Busca e Consulta Ágil</strong></p>

  <img src="Tela_de_Estoque.png" alt="Visualização do Estoque" width="85%"><br>
  <p><strong>💸 Tela de Estoque e Retirada por Venda</strong></p>

  <img src="Tela_de_Relatorio.png" alt="Relatório Geral" width="85%"><br>
  <p><strong>🪵 Relatório Geral e Automação de Perdas</strong></p>

</div>

---

## 🎯 Principais Funcionalidades

* **📊 Painel de Controle Intuitivo:** Interface limpa que exibe alertas preventivos automáticos de produtos com vencimento próximo (configurado para os próximos 30 dias).
* **📥 Inserção e Cadastro Estruturado:** Tela dedicada para entrada de mercadorias registrando nome, código de barras, quantidade, lote, preço de custo, preço de venda e data de validade.
* **🔍 Busca e Consulta Ágil:** Mecanismo de busca dinâmico integrado ao banco de dados que localiza lotes ou produtos instantaneamente por nome.
* **💸 Retirada por Venda e Gestão Financeira:** Baixa automatizada de unidades no estoque físico em tempo real, calculando o faturamento bruto e a margem de lucro gerada a cada operação.
* **🪵 Automação de Perdas:** Regra de negócio backend que identifica produtos expirados, remove-os de circulação e migra os dados para um histórico detalhado de descartes e prejuízos.

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi estruturado priorizando a robustez da lógica backend e a consistência das regras de negócio:

* **Backend:** `Python 3` com o micro-framework `Flask` (altamente flexível e escalável para rotas dinâmicas).
* **Banco de Dados:** `MySQL` (modelagem relacional com controle preciso via tipos estruturados como `DECIMAL` para dados financeiros).
* **Frontend:** `HTML5` / `CSS3` (construção de uma interface limpa, direta e totalmente focada na usabilidade do operador).
* **Lógica de Tempo:** Integração com a biblioteca nativa `datetime` do Python para computar e diferenciar de forma precisa os intervalos de prazos de validade.

---

## 🗄️ Estrutura do Banco de Dados

A arquitetura das tabelas foi planejada para manter o histórico financeiro intacto mesmo após a exclusão ou venda de um produto do estoque físico:

* **`produtos`**: Armazena o estoque atual da loja.
* **`vendas`**: Guarda as transações concluídas e os lucros obtidos.
* **`perdas`**: Registra o impacto financeiro de itens descartados por vencimento.

---

## ⚙️ Foco do Desenvolvimento (Lógica > Estética)

Meu foco era mais voltado para a lógica do projeto e por isso fiz uma interface mais voltada para a usabilidade.


---

## 🚀 Como Executar o Projeto Localmente

1. **Clone o repositório:**
```bash
   git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
