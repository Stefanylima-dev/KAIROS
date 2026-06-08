CREATE DATABASE IF NOT EXISTS sistema_estoqu;
USE sistema_estoqu;

CREATE TABLE produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    codigo_barras VARCHAR(50) NOT NULL DEFAULT '',
    quantidade INT NOT NULL,
    lote INT NOT NULL,
    preco DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    data_validade DATE NOT NULL
);

CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL,
    lote VARCHAR(50),
    preco_venda DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    faturamento_bruto DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    lucro DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE perdas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_produt VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL,
    lote VARCHAR(50),
    preco_custo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    prejuizo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    motivo VARCHAR(255) DEFAULT 'Vencimento',
    data_validade DATE,
    data_perda DATETIME DEFAULT CURRENT_TIMESTAMP
);