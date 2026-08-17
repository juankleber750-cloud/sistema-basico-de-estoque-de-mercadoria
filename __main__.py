from pacotes import db

if __name__ == '__main__':
    banco1 = db()
    banco1.criar_inventario()
    print(banco1.ver_tabela())
    banco1.desligar()
