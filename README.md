Projeto Inventário

Sistema simples de controle de inventário em Python, usando PyMySQL para conexão direta com um banco de dados MySQL.

Sobre o projeto

Este projeto foi criado como estudo de conexão entre Python e MySQL, cobrindo:

- Conexão com banco de dados via `pymysql`
- Criação automática de banco e tabela (`CREATE DATABASE IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`)
- Operações CRUD (Create, Read, Update, Delete) usando uma classe organizada
- Boas práticas de segurança (queries parametrizadas, credenciais fora do código)

Estrutura do banco

Banco: `inventario`

Tabela: `produtos`

| Coluna | Tipo             | Observações                  |
|--------|------------------|-------------------------------|
| id     | INT              | Chave primária, auto increment |
| nome   | VARCHAR(40)      | Único (não permite duplicados) |
| valor  | DECIMAL(5,2)     | Preço do produto              |

Pré-requisitos

- Python 3.10+
- MySQL Server instalado e rodando
- Biblioteca `pymysql`

Instalação da dependência:

```bash
pip install pymysql
```

Configuração das credenciais

As credenciais do banco, não ficam no código-fonte — elas ficam em um arquivo separado (`usuario.py`) que, não é versionado no Git.

1. Crie um arquivo `usuario.py` na raiz do projeto:

```python
user = "root"
senha = "sua_senha_aqui"
host = "localhost"
```

> Nunca suba esse arquivo pro GitHub. Ele contém a senha do seu banco de dados.

Como rodar

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd projeto_01
```

2. Instale as dependências:

```bash
pip install pymysql
```

3. Crie o arquivo `usuario.py` com suas credenciais (veja seção acima).

4. Execute o script principal:

```bash
python3 __main__.py
```

O script vai:
- Criar o banco `inventario` (se ainda não existir)
- Criar a tabela `produtos` (se ainda não existir)
- Executar as operações definidas no código (adicionar, listar, etc.)

Estrutura de código (classe `db`)

O projeto usa uma classe `db` que centraliza a conexão e os métodos de CRUD:

```python
banco1 = db()                              # conecta ao MySQL
banco1.criar_inventario()                  # cria banco + tabela
banco1.adicionar('notebook', 455.78)       # insere um produto
banco1.desligar()                          # fecha a conexão
```

Métodos disponíveis

| Método                          | Ação                                      |
|----------------------------------|--------------------------------------------|
| `criar_inventario()`            | Cria o banco e a tabela, se não existirem  |
| `adicionar(nome, valor)`        | Insere um novo produto                     |
| `atualizar(id, nome, valor)`    | Atualiza um produto existente pelo `id`    |
| `desligar()`                    | Fecha o cursor e a conexão com o banco     |

Observações

- A coluna `nome` é `UNIQUE` — tentar inserir um produto com nome repetido gera erro (`IntegrityError`).
- Todas as queries usam `%s` como placeholder para evitar **SQL Injection**.
- É necessário chamar `.commit()` após qualquer operação de escrita (`INSERT`, `UPDATE`, `DELETE`).

Próximos passos (ideias)

- [ ] Adicionar método `listar()` para consultar todos os produtos
- [ ] Adicionar método `deletar(id)` para remover produtos
- [ ] Criar um menu interativo no terminal
- [ ] Migrar para variáveis de ambiente (`.env`) em vez de `usuario.py`

Tecnologias utilizadas

- [Python 3]
- [PyMySQL]
- [MySQL]
