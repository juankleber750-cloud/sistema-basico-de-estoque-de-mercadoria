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
        if float(valor) >= 0:
            try:
                self.cursor.execute('insert into produtos (nome, valor) values (%s, %s)', (nome, valor))
                self.conexao.commit()
            except pymysql.err.IntegrityError:
                print('produto ja existente no inventario')
        else:
            print('valor invalido')
        
    def atualizar(self, id, nome, valor):
        self.cursor.execute('select count(*) from produtos')
        resultado = (self.cursor.fetchone())[0]
        if int(id) > resultado or int(id) < 0 or resultado == 0:
            print('valor invalido')
        else:
            self.cursor.execute('update produtos set nome = %s, valor = %s where id = %s', (nome, valor, id))
            self.conexao.commit()

    def ver_tabela(self, nome='*', id=None, ordem=None, desc=False):
        self.cursor.execute('select count(*) from produtos')
        resultado = (self.cursor.fetchone())[0]
        if ordem not in ['nome','id','valor', None] or nome not in ['nome','id','valor','*'] or desc != True and desc != False:
            print('valor invalido')
        else:
            if id is not None and (int(id) > resultado or int(id) < 0 or resultado == 0):
                print('valor invalido')
            else:
                if id == None and ordem == None:
                    self.cursor.execute(f'select {nome} from produtos')
                elif id == None and ordem != None and desc == False:
                    self.cursor.execute(f'select {nome} from produtos order by {ordem}')
                elif id != None and ordem != None and desc == False:
                    self.cursor.execute(f'select {nome} from produtos where id = %s order by {ordem}', (id,))
                elif id != None and ordem == None:
                    self.cursor.execute(f'select {nome} from produtos where id = %s', (id,))
                return self.cursor.fetchall()

    def remover(self, id):
        self.cursor.execute('select count(*) from produtos')
        resultado = (self.cursor.fetchone())[0]
        if id is not None and (int(id) > resultado or int(id) < 0 or resultado == 0):
            print('valor invalido')
        else:
            self.cursor.execute('delete from produtos where id = %s', (id,))
            self.conexao.commit()
        
