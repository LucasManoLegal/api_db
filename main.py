# pip install flask_sqlalchemy

# Permite a conexão da API com o banco de dados

# Flask - permite a criação da API com Python

# Response/Request -> Resposta/Requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')

# Rastrear as modificações realizadas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Configuração de conexão com o banco
# %40 - @
# 1 - Usuário (root), 2 - Senha (Senai%40134), 3 - localhost (127.0.0.1), 4 - nome do db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Senai%40134@127.0.0.1/db_carro'

mydb = SQLAlchemy(app)

# Classe para definir o modelo dos dados que correspondem a tabeala do banco de dados
class Carros(mydb.Model):
    __tablename__ = 'tb_carro'
    id_carro = mydb.Column(mydb.Integer, primary_key= True)
    marca = mydb.Column(mydb.String(100))
    modelo = mydb.Column(mydb.String(100))
    ano = mydb.Column(mydb.Integer)
    valor = mydb.Column(mydb.String(100))
    cor = mydb.Column(mydb.String(100))
    numero_vendas = mydb.Column(mydb.Integer)

    # Essa função vai ser utilizadas para converter o objeto em json
    def to_json(self):
        return {
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "cor": self.cor,
            "numero_vendas": self.numero_vendas
        }
    
# MÉTODO 1 - GET
@app.route('/carros', methods=['GET'])

def ver_carros():
    carros_selecionados = Carros.query.all()
    carros_json = [carro.to_json() for carro in carros_selecionados]
    return gera_resposta(200, 'Carros', carros_json)

# MÉTODO 1.1 - GET (POR ID)
@app.route('/carros/<int:id_selecionado>', methods=['GET'])

def seleciona_carro_id(id_selecionado):
    carro_selecionado = Carros.query.filter_by(id_carro = id_selecionado).first()
    carro_json = carro_selecionado.to_json()
    return gera_resposta(200, "Carro selecionado", carro_json, "Carro encontrado!")

# MÉTODO 2 - POST
@app.route('/carros', methods=['POST'])

def criar_carro():
    requisicao = request.get_json()

    try:
        carro = Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor = requisicao['cor'],
            numero_vendas = requisicao['numero_vendas']
        )
        # Adiciona ao banco (session.add)
        mydb.session.add(carro)
        # Salva no banco (session.commit)
        mydb.session.commit()

        return gera_resposta(201, 'Novo carro:', carro.to_json(), 'Carro criado com sucesso!')

    except Exception as e:
        print('Erro:', e)
        return gera_resposta(400, 'Erro.', {}, 'Erro ao cadastrar!')
    
# MÉTODO 3 - DELETE
@app.route('/carros/<int:id_selecionado>', methods=['DELETE'])
def excluir_carro(id_selecionado):
    carro = Carros.query.filter_by(id_carro = id_selecionado).first()
    try:
        mydb.session.delete(carro)
        mydb.session.commit()
        return gera_resposta(200, 'Carro Excluído', carro.to_json(), 'Carro excluído com sucesso!')
    except Exception as e:
        print('Erro:', e)
        return gera_resposta(400, 'Erro.', {}, 'Erro ao excluir.')

# MÉTODO 4 - PUT
@app.route('/carros/<int:id_selecionado>', methods=['PUT'])
def atualizar_carro(id_selecionado):
    carro = Carros.query.filter_by(id_carro = id_selecionado).first()
    requisicao = request.get_json()

    try:
        if ('marca' in requisicao):
            carro.marca = requisicao['marca']

        if ('modelo' in requisicao):
            carro.modelo = requisicao['modelo']

        if ('ano' in requisicao):
            carro.ano = requisicao['ano']

        if ('valor' in requisicao):
            carro.valor = requisicao['valor']

        if ('cor' in requisicao):
            carro.cor = requisicao['cor']

        if ('numero_vendas' in requisicao):
            carro.numero_vendas = requisicao['numero_vendas']

        mydb.session.add(carro)
        mydb.session.commit()

        return gera_resposta(200, 'Valor Novo', carro.to_json(), 'Carro atualizado!')
    except Exception as e:
        print('Erro', e)
        return gera_resposta(400, 'Erro.', {}, 'Erro ao atualizar carro.')

# RESPOSTA PADRÃO
def gera_resposta(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if(mensagem):
        body['mensagem'] = mensagem
    # Dumps - Converte o dicionario criado (body) em JSON (json.dumps)
    return Response(json.dumps(body), status=status, mimetype='application/json')

app.run(port=5000, host="localhost", debug=True)

