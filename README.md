# Sistema Básico de Estoque de Mercadoria

Sistema simples de controle de estoque em Python, usando **PyMySQL** para conexão direta com um banco de dados **MySQL**.

> Depois de um tempo estudando sobre MySQL, consegui montar esse pequeno sistema de estoque de produtos em Python com PyMySQL.

## 📋 Sobre o projeto

Este projeto foi criado como estudo de conexão entre Python e MySQL, cobrindo:

- Conexão com banco de dados via `pymysql`
- Criação automática de banco e tabela (`CREATE DATABASE IF NOT EXISTS`, `CREATE TABLE IF NOT EXISTS`)
- Operações CRUD (Create, Read, Update, Delete) usando uma classe organizada
- Validações de entrada (valores negativos, IDs inexistentes, colunas inválidas)
- Boas práticas de segurança (queries parametrizadas, credenciais fora do código)

## 🗂️ Estrutura do banco

**Banco:** `inventario`

**Tabela:** `produtos`

| Coluna | Tipo             | Observações                    |
|--------|------------------|----------------------------------|
| id     | INT              | Chave primária, auto increment   |
| nome   | VARCHAR(40)      | Único (não permite duplicados)   |
| valor  | DECIMAL(5,2)     | Preço do produto                 |

## ⚙️ Pré-requisitos

- Python 3.10+
- MySQL Server instalado e rodando
- Biblioteca `pymysql`

Instalação da dependência:

```bash
pip install pymysql
```

## 🔐 Configuração das credenciais

As credenciais do banco **não ficam no código-fonte** — elas ficam em um arquivo separado (`usuario.py`) que **não é versionado no Git**.

1. Crie um arquivo `usuario.py` na raiz do projeto:

```python
user = "root"
senha = "sua_senha_aqui"
host = "localhost"
```

2. Garanta que esse arquivo está no `.gitignore`:

```
usuario.py
```

> ⚠️ **Nunca suba esse arquivo pro GitHub.** Ele contém a senha do seu banco de dados.

## 🚀 Como rodar

1. Clone o repositório:

```bash
git clone https://github.com/juankleber750-cloud/sistema-basico-de-estoque-de-mercadoria
cd sistema-basico-de-estoque-de-mercadoria
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

## 🧱 Estrutura de código (classe `db`)

O projeto usa uma classe `db` que centraliza a conexão e os métodos de CRUD:

```python
banco1 = db()                              # conecta ao MySQL
banco1.criar_inventario()                  # cria banco + tabela
banco1.adicionar('notebook', 3499.90)      # insere um produto
banco1.ver_tabela()                        # consulta os produtos
banco1.atualizar(1, 'notebook gamer', 4599.90)  # atualiza um produto
banco1.remover(2)                          # remove um produto
banco1.desligar()                          # fecha a conexão
```

### Métodos disponíveis

| Método                                        | Ação                                                                 |
|------------------------------------------------|-----------------------------------------------------------------------|
| `criar_inventario()`                           | Cria o banco e a tabela, se não existirem                            |
| `adicionar(nome, valor)`                       | Insere um novo produto (bloqueia valores negativos e nomes duplicados) |
| `atualizar(id, nome, valor)`                   | Atualiza um produto existente pelo `id`, validando se o `id` existe   |
| `ver_tabela(nome='*', id=None, ordem=None, desc=False)` | Consulta produtos, com filtros opcionais por coluna, id e ordenação |
| `remover(id)`                                  | Remove um produto pelo `id`, validando se ele existe                 |
| `desligar()`                                   | Fecha o cursor e a conexão com o banco                                |

### Detalhes do `ver_tabela()`

O método aceita parâmetros opcionais para consultas mais flexíveis:

```python
banco1.ver_tabela()                          # todas as colunas, todos os produtos
banco1.ver_tabela(nome='nome')               # só a coluna 'nome'
banco1.ver_tabela(id=1)                      # só o produto com id=1
banco1.ver_tabela(ordem='valor')             # todos, ordenados por valor
```

- `nome`: qual coluna retornar (`'nome'`, `'id'`, `'valor'` ou `'*'` para todas)
- `id`: filtra por um produto específico
- `ordem`: ordena o resultado por uma coluna válida
- `desc`: ⚠️ **em desenvolvimento** — a ideia é permitir ordenação decrescente (`ORDER BY ... DESC`), mas essa parte ainda não está implementada nas queries

Todos os parâmetros passam por validação antes de montar a consulta, evitando valores inválidos ou nomes de coluna não permitidos.

## ⚠️ Observações

- A coluna `nome` é `UNIQUE` — tentar inserir um produto com nome repetido gera erro tratado (`IntegrityError`).
- `adicionar()` bloqueia valores negativos antes mesmo de tentar inserir no banco.
- `atualizar()` e `remover()` verificam se o `id` informado existe antes de executar a operação.
- Nomes de colunas (`nome`, `ordem`) são inseridos via f-string, mas **sempre validados antes** contra uma lista fixa de valores permitidos — o que evita SQL Injection mesmo sem usar `%s` nesses casos.
- Valores (dados) sempre usam `%s` como placeholder.
- É necessário chamar `.commit()` após qualquer operação de escrita (`INSERT`, `UPDATE`, `DELETE`).

## 📌 Próximos passos (ideias)

- [ ] Finalizar a implementação do parâmetro `desc` no `ver_tabela()` (ordenação decrescente)
- [ ] Criar um menu interativo no terminal
- [ ] Migrar para variáveis de ambiente (`.env`) em vez de `usuario.py`
- [ ] Adicionar testes automatizados

## 🛠️ Tecnologias utilizadas

- [Python 3](https://www.python.org/)
- [PyMySQL](https://pymysql.readthedocs.io/)
- [MySQL](https://www.mysql.com/)
