# Sistema Básico de Estoque de Mercadoria

Sistema simples de controle de estoque em Python, utilizando a biblioteca PyMySQL para integração e persistência de dados em um banco de dados MySQL.

> Este projeto foi desenvolvido como objeto de estudo prático sobre modelagem de bancos de dados, conexões relacionais com PyMySQL e arquitetura de operações CRUD no ecossistema Python.

---

## 🚀 Sobre o Projeto

O sistema centraliza o gerenciamento de produtos através de uma classe encapsulada chamada `db`, garantindo que todas as regras de negócio e validações ocorram antes ou durante a persistência dos dados.

### Principais aprendizados cobertos:
- Conexão e manipulação do banco de dados via `pymysql`.
- Automação de infraestrutura estrutural (`CREATE DATABASE` e `CREATE TABLE` condicionais).
- Operações CRUD completas (Create, Read, Update, Delete) centralizadas em uma única classe.
- Validações de consistência lógica (bloqueio de valores negativos, tratamento de IDs inexistentes, restrição de colunas).
- Segurança de dados contra SQL Injection utilizando queries parametrizadas (`%s`).

---

## 📊 Estrutura do Banco de Dados

O sistema cria e gerencia de forma autônoma o banco de dados `inventario` contendo a tabela `produtos`:

| Coluna | Tipo             | Propriedades e Regras de Negócio |
|--------|------------------|----------------------------------|
| `id`     | INT              | Chave primária, Auto Incremento. |
| `nome`   | VARCHAR(40)      | Único (`UNIQUE`). Não aceita duplicidade de produtos. |
| `valor`  | DECIMAL(5,2)     | Preço do produto. Bloqueia inserção de valores < 0. |

---

## 🛠️ Pré-requisitos e Dependências

- Python 3.10 ou superior
- MySQL Server (ativo e rodando localmente)
- Biblioteca `pymysql`

Instale a dependência obrigatória executando no terminal:
```bash
pip install pymysql
```

---

## 🔐 Configuração das Credenciais (Segurança)

Como boa prática de segurança, as credenciais de acesso ao seu servidor de banco de dados ficam isoladas em um módulo separado chamado `usuario.py`. **Certifique-se de adicionar este arquivo ao seu `.gitignore`** para não expor suas senhas publicamente.

Crie o arquivo `usuario.py` na raiz do seu projeto com o seguinte conteúdo:

```python
user = "seu_usuario_do_mysql"
senha = "sua_senha_do_mysql"
host = "localhost"
```

---

## ⚡ Como Executar o Projeto

1. Certifique-se de que o seu servidor MySQL esteja rodando.
2. Clone o repositório ou navegue até a pasta do projeto:
   ```bash
   cd caminho/para/o/projeto_01
   ```
3. Garanta que o arquivo `usuario.py` esteja configurado.
4. Execute o arquivo de ponto de entrada do sistema:
   ```bash
   python3 __main__.py
   ```

---

## 🧠 Arquitetura do Código (Classe `db`)

A classe `db` abstrai toda a complexidade SQL em métodos Python limpos. Veja como interagir com ela no seu código principal:

```python
from database import db # Supondo que a classe esteja em database.py

# 1. Instancia a classe e abre as conexões com o MySQL
banco = db()

# 2. Cria a infraestrutura inicial do banco se não existir
banco.criar_inventario()

# 3. Adiciona produtos validando integridade
banco.adicionar('Teclado Mecânico', 249.90)
banco.adicionar('Mouse Gamer', 189.50)

# 4. Consulta a tabela de diferentes maneiras
produtos = banco.ver_tabela()
print(produtos)

# 5. Atualiza dados de um produto existente pelo ID
banco.atualizar(1, 'Teclado RGB', 279.90)

# 6. Remove um item pelo ID
banco.remover(2)

# 7. Sempre feche os cursores e conexões ao finalizar
banco.desligar()
```

---

## 📖 Documentação dos Métodos

| Método | Assinatura | Comportamento e Validações |
|--------|------------|----------------------------|
| **`criar_inventario`** | `criar_inventario()` | Cria o schema `inventario` e a tabela `produtos` caso não existam no servidor. |
| **`adicionar`** | `adicionar(nome, valor)` | Insere um novo registro. Bloqueia valores negativos e trata o erro `IntegrityError` se o nome do produto já existir. |
| **`atualizar`** | `atualizar(id, nome, valor)` | Modifica o nome e valor de um item existente. Valida se o `id` é positivo e se ele realmente existe na base antes de executar o `UPDATE`. |
| **`remover`** | `remover(id)` | Deleta de forma permanente um registro pelo `id`. Exibe mensagem de erro caso o ID informado não conste na tabela. |
| **`ver_tabela`** | `ver_tabela(nome='*', id=None, ordem=None, desc=False)` | Recupera dados customizáveis através de filtros de coluna, ID específico e ordenações avançadas. |
| **`desligar`** | `desligar()` | Finaliza com segurança os buffers abertos do cursor e a conexão ativa com o banco de dados. |

### Detalhes Avançados do Método `ver_tabela()`

O método de leitura foi projetado para aceitar múltiplos filtros opcionais de forma extremamente flexível:

* **Filtrar colunas específicas:** `banco.ver_tabela(nome='nome')` (retorna apenas a lista de nomes).
* **Filtrar por ID único:** `banco.ver_tabela(id=5)`.
* **Ordenar resultados:** `banco.ver_tabela(ordem='valor')` (ordena de forma crescente pelo preço).
* **Ordenação Decrescente:** `banco.ver_tabela(ordem='valor', desc=True)` (ordena do mais caro para o mais barato).

*Nota de Segurança:* Para evitar vulnerabilidades de SQL Injection no nome de colunas e cláusulas de ordenação (onde o operador `%s` não pode ser usado nativamente), o método valida os argumentos contra uma lista estrita de strings permitidas antes de renderizar a query.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **PyMySQL** (Driver de conexão nativo)
- **MySQL Server** (Banco de dados relacional)
