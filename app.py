# coding=utf-8

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json 

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import OLX

data = {
	"phone_number":"(68) 99974 8004",
	"city":"Rio Branco",
	"sub_category":"Notebook e netbook",
	"title":"Dell",
	"main_image_urls":["http://img.olx.com.br/images/91/910712038681161.jpg"],
	"adcode":"376381384",
	"main_category":"eletronicos-e-celulares",
	"zipcode":"69914-362",
	"image_urls":["http://img.olx.com.br/images/91/910712038681161.jpg",
	"http://img.olx.com.br/images/91/915712030105770.jpg",
	"http://img.olx.com.br/images/91/910712037593319.jpg"],
	"month":"Agosto",
	"phone":"http://static.bn-static.com/pg/0HxzsfNvMlSr0Fq6RGNDyGocoIf4+B89CKwXOCA1pRw==.gif",
	"suburb":"Santa Quitéria",
	"ads":"http://ac.olx.com.br/acre/computadores-e-acessorios/dell-376381384",
	"time":"07:38",
	"price":"R$1.700",
	"name":"Negociador",
	"day":"13",
	"novo_usado":"",
	"description":"Notebook Dell vostro 3550 com algumas melhorias.Tela de 15 polegadasProcessador i5 de 2.5 GHz com tubo boster alcança\naté 3.1 GHz.12 gigas de memória ram.HD SSD 240 GBPlaca Intel(R) HD Graphics 3000Teclado retro iluminadoBluetoothWi-FiWeb CamLeitor de cartãoLeitor biométricoHDMIGravador de CD/ DVDWindows 7 OBS: Bateria está viciadaNotebook reinicia em 7 segundos ótimo para\nprogramas pesados tipo Corel draw e entre outro\npesados de edição e jogos também. Em perfeito\nestado de conservação.Para vender logo quem conhece de computador sabe\nque está no preçoNetbook, PC, Computador, micro, computador de\nmesa, PC Gamer"
}


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/post_data', methods=['GET', 'POST'])
def post_data():
	if request.method == "POST":
		if not request.json:
			abort(400)
		json_dict = request.get_json()
		print(json_dict)
		olx = OLX(**json_dict)
		db.session.add(olx)
		db.session.commit()
		return jsonify({'success': True}), 201

@app.route('/fetch_data/', methods=['GET', 'POST'])
def fetch_data():
	limit = int(request.args.get('limit', 100))
	if request.method == "GET":
		olxs = OLX.query.limit(limit).all()
		return json.dumps(OLX.serialize_list(olxs))
if __name__ == '__main__':
    app.run()