# 📦 Sistema de Inventário & API de Controle de Estoque

Este projeto é um sistema simples e robusto de controle de estoque desenvolvido em **Python**. Ele expõe uma **API REST utilizando Flask** e gerencia a persistência de dados em um banco de dados relacional **MySQL** por meio da biblioteca **PyMySQL**.

O projeto foi construído separando rigidamente a camada de persistência de dados (módulo do banco) da camada de transporte e rotas (API HTTP).

---

## 🚀 Funcionalidades

- **Criação Autônoma**: Na primeira execução, o sistema cria automaticamente o banco de dados (`inventario`) e a tabela (`produtos`) caso ainda não existam no servidor.
- **Segurança contra SQL Injection**: Uso estrito de queries parametrizadas (`%s`) e validação de strings (*whitelist*) para o nome de colunas e parâmetros dinâmicos.
- **Camada de Validação**: Bloqueio de valores negativos para preços, prevenção de duplicações usando restrição `UNIQUE` e tratamento amigável de erros.
- **API REST Completa (CRUD)**: Endpoints HTTP configurados para criar, ler, atualizar e excluir produtos.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12.3**
- **Flask** (Framework Web / API)
- **PyMySQL** (Driver de conexão com o banco de dados)
- **Python-Dotenv** (Gerenciamento de variáveis de ambiente)
- **MySQL Server** (Banco de dados relacional)

---

## 📊 Estrutura do Banco de Dados

O banco de dados gerado se chama `inventario` e possui a tabela `produtos` estruturada da seguinte forma:

| Coluna | Tipo | Propriedades e Regras de Negócio |
| :--- | :--- | :--- |
| `id` | INT | Chave primária, Auto Incremento. |
| `nome` | VARCHAR(40) | Único (`UNIQUE`). Não aceita produtos duplicados. |
| `valor` | DECIMAL(5,2) | Preço do produto. Bloqueia inserções de valores menores que zero. |

---

## 🔧 Pré-requisitos e Instalação

1. Certifique-se de ter o **Python 3** e o **MySQL Server** instalados e ativos em sua máquina local.
2. Clone este repositório no seu ambiente de desenvolvimento:
   ```bash
   git clone https://github.com
   cd sistema-basico-de-estoque-de-mercadoria
   ```
3. Crie e ative um ambiente virtual (`venv`):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências necessárias:
   ```bash
   pip install flask pymysql python-dotenv
   ```

---

## 🔐 Configuração das Credenciais

As credenciais do banco de dados ficam isoladas em um arquivo de variáveis de ambiente por motivos de segurança.

1. Copie o arquivo de exemplo **`.env.example`** e renomeie a cópia para **`.env`** na raiz do projeto:
   ```bash
   cp .env.example .env
   ```
2. Abra o arquivo **`.env`** e preencha os dados de acesso do seu MySQL local:
   ```env
   DB_USER=seu_usuario_do_mysql
   DB_PASSWORD=sua_senha_do_mysql
   DB_HOST=localhost
   DB_PORT=3306
   ```

---

## ⚡ Como Executar

Com o servidor MySQL rodando, o ambiente virtual ativo e o arquivo `.env` configurado, inicie a aplicação:

```bash
python3 __main__.py
```

A API estará rodando por padrão em: `http://127.0.0.1:5000`

---

## 🗺️ Documentação da API (Endpoints)

A API aceita os seguintes parâmetros via Query String (`?parâmetro=valor`) nas requisições:

### 1. Listar / Buscar Produtos
* **Rota:** `/tabela`
* **Método:** `GET`
* **Parâmetros Opcionais:**
  * `nome`: Especifica colunas que deseja retornar (`nome`, `id`, `valor` ou `*`).
  * `id`: Filtra as informações de um ID único de produto.
  * `ordem`: Ordena por uma coluna específica (`id`, `nome` ou `valor`).
  * `desc`: Caso queira a ordenação decrescente, defina como `true`.

### 2. Adicionar Produto
* **Rota:** `/tabela`
* **Método:** `POST`
* **Parâmetros Obrigatórios:** `nome` e `valor`
* **Exemplo:** `POST /tabela?nome=Teclado&valor=150.00`

### 3. Atualizar Produto
* **Rota:** `/tabela`
* **Método:** `PUT`
* **Parâmetros Obrigatórios:** `id`, `nome` e `valor`
* **Exemplo:** `PUT /tabela?id=1&nome=Teclado%20Mecanico&valor=250.00`

### 4. Remover Produto
* **Rota:** `/tabela/<id>`
* **Método:** `DELETE`
* **Exemplo:** `DELETE /tabela/5` (remove o produto com ID 5).

