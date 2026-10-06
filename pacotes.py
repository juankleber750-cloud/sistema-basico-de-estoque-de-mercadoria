from usuario import user, senha, host
import pymysql


class db():
    def __init__(self):
        self.conexao = pymysql.connect(user=user, password=senha, host=host, port=3306)
        self.cursor = self.conexao.cursor()

    def desligar(self):
        '''
        desliga a conexão do pymysql com o mysql
        evitando assim possiveis bugs em codigos muito grandes
        '''
        self.cursor.close()
        self.conexao.close()

    def criar_inventario(self):
        '''
        cria o banco de Dados 'inventario' e a tabela 'produtos'
        '''
        self.cursor.execute('create database if not exists inventario')
        self.cursor.execute('use inventario')
        self.cursor.execute('create table if not exists produtos (id int auto_increment primary key, nome varchar(40) unique, valor decimal(5, 2))')

    def adicionar(self, nome, valor):
        '''
        adiciona o produto que deseja na tabela 'produtos'
        nome = 'nome'
        valor = 'valor' (o valor atribuido ao produto pode ser inteiro ou decimal)
        id = o id é altomaticamente incrementado na tabela
        '''
        if float(valor) >= 0:
            try:
                self.cursor.execute('insert into produtos (nome, valor) values (%s, %s)', (nome, valor))
                self.conexao.commit()
            except pymysql.err.IntegrityError:
                return {
                'status': 'produto ja existente no inventario'
                }

        else:
            return {
            'status': 'valor invalido'
            }
        
    def atualizar(self, id, nome, valor):
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None and id != None:
            return {
            'status':'id inexistente'
            }

        elif id != None and produto != None:
            self.cursor.execute('update produtos set nome = %s, valor = %s where id = %s', (nome, valor, id))
            self.conexao.commit()

    def ver_tabela(self, nome='*', id=None, ordem=None, desc=False):
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None and id != None:
            return 'id inexistente'

        elif id != None and produto != None:
            if ordem not in ['nome','id','valor', None] or nome not in ['nome','id','valor','*'] or desc != True and desc != False:
                return {
                'status': 'valor invalido'
                }

            else:
                if ordem != None and desc == False:
                    self.cursor.execute(f'select {nome} from produtos where id = %s order by {ordem}', (id,))
                elif ordem != None and desc == True:
                    self.cursor.execute(f'select {nome} from produtos where id = %s order by {ordem} desc', (id,))
                elif ordem == None:
                    self.cursor.execute(f'select {nome} from produtos where id = %s', (id,))

        elif id == None:
            if ordem not in ['nome','id','valor', None] or nome not in ['nome','id','valor','*'] or desc != True and desc != False:
                return {
                'status': 'valor invalido'
                }

            else:
                if ordem == None:
                    self.cursor.execute(f'select {nome} from produtos')
                elif ordem != None and desc == False:
                    self.cursor.execute(f'select {nome} from produtos order by {ordem}')
                elif ordem != None and desc == True:
                    self.cursor.execute(f'select {nome} from produtos order by {ordem} desc')

        return self.cursor.fetchall()

    def remover(self, id):
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None and id != None:
            return {
            'status': 'id inexistente'
            }

        elif produto != None and id != None:
            self.cursor.execute('delete from produtos where id = %s', (id,))
            self.conexao.commit()
