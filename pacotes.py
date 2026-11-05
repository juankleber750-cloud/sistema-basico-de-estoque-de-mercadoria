from usuario import user, senha, host
import pymysql


class db():
    def __init__(self):
        self.conexao = pymysql.connect(user=user, password=senha, host=host, port=3306)
        self.cursor = self.conexao.cursor(pymysql.cursors.DictCursor)
        
    def __enter__(self):
        self.cursor.execute('create database if not exists inventario')
        self.cursor.execute('use inventario')
        self.cursor.execute('create table if not exists produtos (id int auto_increment primary key, nome varchar(40) unique, valor decimal(5, 2), constraint valor_positivo check (valor >= 0))')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        desliga a conexão do pymysql com o mysql
        evitando assim possiveis bugs em codigos muito grandes
        '''
        self.cursor.close()
        self.conexao.close()

    def adicionar(self, nome: str, valor: str) -> dict:
        '''
        adiciona o produto que deseja na tabela 'produtos'
        nome = 'nome_do_produto'
        valor = '999.90' (o valor atribuido ao produto pode ser inteiro ou decimal)
        id = o id é altomaticamente incrementado na tabela
        '''
        try:
            valor = valor.replace(',', '.')
            if float(valor) < 0:
                return {'status': 'valor invalido'}
        except (ValueError, AttributeError):
            return {'status': 'valor invalido'}

        try:
            self.cursor.execute('insert into produtos (nome, valor) values (%s, %s)', (nome, valor))
            self.conexao.commit()
        except pymysql.err.IntegrityError:
            return {'status': 'produto ja existente no inventario'}

        return {'status': 'produto adicionado com sucesso'}
        
    def atualizar(self, id: str, nome: str, valor: str) -> dict:
        '''
        altera o nome e valor através de um id existente
        as variaveis id, nome e valor são parâmetros obrigatórios
        '''
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None:
            return {
            'status':'produto não encontrado'
            }

        try:
            valor = valor.replace(',', '.')
            if float(valor) < 0:
                return {'status': 'valor invalido'}
        except (ValueError, AttributeError):
            return {'status': 'valor invalido'}
           
        self.cursor.execute('update produtos set nome = %s, valor = %s where id = %s', (nome, valor, id))
        self.conexao.commit()

        return {
        'status': 'produto alterado com sucesso'
        }

    def ver_tabela(self, nome: str ='*', id: str | None = None, ordem: str | None = None, desc: bool = False) -> list | dict:
        '''
        a função ver_tabela retorna as informações dos itens cadastrados na tabela
        a função contem 4 parâmetros não obrigatorios sendo eles nome, id, ordem e desc
        o parâmetro nome por padrão vai ser atribuido a '*' oq vai fazer a função ver tabela retornar todas as colunas (id, nome, valor)
        o parâmetro id por padrão vai ser atribuido a None, qualquer valor diferente que None que esteja na tabela retornará apenas aquele item
        o parâmetro ordem vem atribuido por padrão a o valor None, voçê pode atribuir o valor dele a qualquer coluna da tabela ('id', 'nome', 'valor'), adicionar um valor diferente de None fará a função retornar o select ordenado seja por ordem alfabetica ou numerica
        o parâmetro desc vem atribuido por padrão a o valor False, colocar um valor booleano diferente que Falso fará ele inverter a ordem do select
        obs: o parâmetro desc so funciona se o parâmetro ordem for diferente que None

        os valores disponiveis para cada parâmetro são:
        nome: ('nome', 'id', 'valor', '*')
        id: (None, e qualquer numero inteiro)
        ordem: ('nome', 'id', 'valor', None)
        desc: (False, True)
        '''
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None and id != None:
            return {
            'status':'id inexistente'
            }

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

                return self.cursor.fetchone()

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

    def remover(self, id: str) -> dict:
        '''
        usa um parâmetro obrigatório (id) para excluir um item do banco de dados
        caso o id não exista a função retornara uma mensagem dict informando o erro
        '''
        self.cursor.execute('select id from produtos where id = %s', (id,))
        produto = self.cursor.fetchone()
        if produto == None and id != None:
            return {
            'status': 'id inexistente'
            }

        self.cursor.execute('delete from produtos where id = %s', (id,))
        self.conexao.commit()

        return {
        'status': 'produto removido com sucesso'
        }
