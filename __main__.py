from flask import Flask, jsonify, request
from pacotes import DB

app = Flask(__name__)

@app.route('/tabela/', methods=['GET'])
@app.route('/tabela/<id>', methods=['GET'])
def ver_tabela(id=None):
    coluna_nome = request.args.get('nome', '*')
    ordenar_por = request.args.get('ordem', None)
    valores_desc = request.args.get('desc', 'false').lower()
    valores_desc = True if valores_desc == 'true' else False

    with DB() as banco:
        status = banco.ver_tabela(nome=coluna_nome, id=id, ordem=ordenar_por, desc=valores_desc)

    if type(status) == dict:
        if status.get('status') != 'id inexistente' and status.get('status') != 'valor invalido':
            return jsonify(status)
        elif status.get('status') == 'valor invalido':
            return jsonify({'erro': 'valor fornecido invalido'}), 400
        return jsonify({'erro': 'produto não encontrado'}), 404

    return jsonify(status)

@app.route('/tabela', methods=['POST'])
def adicionar_produto():
    dados = request.get_json()
    produto_nome = dados.get('nome')
    produto_valor = dados.get('valor')

    with DB() as banco:
        status = banco.adicionar(nome=produto_nome, valor=produto_valor)
    
    if status.get('status') == 'valor invalido':
        return jsonify({'erro': 'valor fornecido invalido'}), 400
    elif status.get('status') == 'produto ja existente no inventario':
        return jsonify({'error': 'Conflito', 'message': 'este produto já está cadastrado.'}), 409

    return jsonify(status)

@app.route('/tabela/<id>', methods=['PUT'])
def alterar_produto(id):
    dados = request.get_json()
    produto_nome = dados.get('nome')
    produto_valor = dados.get('valor')

    with DB() as banco:
        status = banco.atualizar(id=id, nome=produto_nome, valor=produto_valor)

    if status.get('status') == 'produto não encontrado':
        return jsonify({'erro': 'produto não encontrado'}), 404

    elif status.get('status') == 'valor invalido':
        return jsonify({'erro': 'valor fornecido invalido'}), 400
        
    return jsonify(status)

@app.route('/tabela/<id>', methods=['DELETE'])
def remover_produto(id):
    with DB() as banco:
        status = banco.remover(id=id)
    
    if status.get('status') == 'produto removido com sucesso':
        return jsonify(status)

    return jsonify({'erro': 'produto não encontrado'}), 404

if __name__ == '__main__':        
    app.run(debug=True)
