from usuario import user, senha, host
import pymysql

class db():
    def __init__(self):
        self.conexao = pymysql.connect(user=user, password=senha, host=host, port=3306)
        self.cursor = self.conexao.cursor()

    def desligar(self):
        self.cursor.close()
        self.conexao.close()

    def criar_inventario(self):
        self.cursor.execute('create database if not exists inventario')
        self.cursor.execute('use inventario')
        self.cursor.execute('create table if not exists produtos (id int auto_increment primary key, nome varchar(40) unique, valor decimal(5, 2))')

    def adicionar(self, nome, valor):
        self.cursor.execute('insert into produtos (nome, valor) values (%s, %s)', (nome, valor))    
        self.conexao.commit()
        
    def atualizar(self, id, nome, valor):
        self.cursor.execute('update produtos set nome = %s, valor = %s where id = %s', (nome, valor, id))
        self.conexao.commit()

    def ver_tabela(self):
        self.cursor.execute('select * from produtos')
        return self.cursor.fetchall()
