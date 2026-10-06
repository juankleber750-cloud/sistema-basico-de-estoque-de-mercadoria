from flask import Flask, jsonify
from pacotes import db

app = Flask(__name__)

banco_inicial = db()
banco_inicial.criar_inventario()
banco_inicial.desligar()

@app.route("/tabela/<id>")
def tabela(id):
    banco1 = db()
    resultado = banco1.ver_tabela(nome='*', id=id)
    if resultado:
        produto = resultado[0]

    if resultado:
        jsonify({'erro': 'produto não encontrado'}), 404

    return jsonify({"id": produto[0],"nome": produto[1],"valor": float(produto[2])})

app.run(debug=True)
