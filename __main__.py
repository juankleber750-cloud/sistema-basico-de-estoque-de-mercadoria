from pacotes import db

if __name__ == '__main__':
    banco1 = db()
    banco1.criar_inventario()
    banco1.adicionar(nome='rapadura', valor='32.99')
    banco1.adicionar(nome='beijinho', valor='12.50')
    print(banco1.ver_tabela(nome='*',ordem='nome', desc=False))
    banco1.desligar()
