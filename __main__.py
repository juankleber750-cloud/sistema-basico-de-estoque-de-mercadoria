from flask import Flask, jsonify, request
from pacotes import db

app = Flask(__name__)

@app.route('/tabela', methods=['GET'])
def ver_tabela():
    coluna_nome = request.args.get('nome', '*')
    produto_id = request.args.get('id', None)
    ordenar_por = request.args.get('ordem', None)
    valores_desc = request.args.get('desc', 'false').lower()
    valores_desc = True if valores_desc == 'true' else False

    banco = db()
    banco.criar_inventario()
    status = banco.ver_tabela(nome=coluna_nome, id=produto_id, ordem=ordenar_por, desc=valores_desc)
    banco.desligar()

    if type(status) == dict:
        if status.get('status') != 'id inexistente' and status.get('status') != 'valor invalido':
            return jsonify(status)

        return jsonify({'erro': 'produto não encontrado'}), 404

    return jsonify(status)

@app.route('/tabela', methods=['POST'])
def adicionar_produto():
    produto_nome = request.args.get('nome')
    produto_valor = request.args.get('valor')

    banco = db()
    banco.criar_inventario()
    status = banco.adicionar(nome=produto_nome, valor=produto_valor)

    if status.get('status') == 'valor invalido':
        return jsonify({'erro': 'valor fornecido invalido'}), 400
    elif status.get('status') == 'produto ja existente no inventario':
        return jsonify({'error': 'Conflito', 'message': 'este produto já está cadastrado.'}), 409

    return jsonify(status)

@app.route('/tabela', methods=['PUT'])
def alterar_produto():
    produto_id = request.args.get('id')
    produto_nome = request.args.get('nome')
    produto_valor = request.args.get('valor')

    banco = db()
    banco.criar_inventario()
    status = banco.atualizar(id=produto_id, nome=produto_nome, valor=produto_valor)

    
    if status.get('status') == 'produto não encontrado':
        return jsonify({'erro': 'produto não encontrado'}), 404

    return jsonify(status)

@app.route('/tabela/<id>', methods=['DELETE'])
def remover_produto(id):
    banco = db()
    banco.criar_inventario()
    status = banco.remover(id=id)

    if status.get('status') == 'produto removido com sucesso':
        return jsonify(status)

    return jsonify({'erro': 'produto não encontrado'}), 404

if __name__ == '__main__':        
    app.run(debug=True)
