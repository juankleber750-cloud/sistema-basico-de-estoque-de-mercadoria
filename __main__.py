from pacotes import db

if __name__ == '__main__':
    banco1 = db()
    banco1.criar_inventario()
    banco1.adicionar('arroz', '39.50')
    banco1.adicionar('feijão', '11.50')
    banco1.atualizar('1', 'arroz', '39.00')
    print(banco1.ver_tabela(ordem='nome', desc=False))
    banco1.desligar()
