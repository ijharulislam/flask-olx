# coding=utf-8

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import json 

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
POSTGRES = {
    'user': 'olx',
    'pw': 'plx-spider',
    'db': 'olx',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

from models import OLX

"""the other usecase of the other developer is that he will choose, in our own system, the existing city and suburbs that comes from your api . Then after choosed the suburbs he wants he clicks in Submit and then he gets from the choosed suburbs the following fields of their itens:phone, username, ad title, ad posting date and main categ. Need to know what is the best format to receive these data to our system
and in my case i need to have a page where i can select city/suburbs and the fields i want and download it as csv"""

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
	phone = request.args.get('phone', None)
	adcode = int(request.args.get('adcode', None))
	suburbs = int(request.args.get('suburbs', None))
	city = int(request.args.get('city', None))

	if request.method == "GET":
		olxs = []
		if phone or adcode:
			olxs = OLX.query.limit(limit).filter(OLX.phone_number=phone).all()|OLX.query.limit(limit).filter(OLX.adcode=adcode).all()
		if city and suburbs:
			olxs = OLX.query.limit(limit).filter(OLX.city=city, OLX.suburb=suburb).all()
		elif city or suburbs:
			olxs = OLX.query.limit(limit).filter(OLX.city=city).all()|OLX.query.limit(limit).filter(OLX.suburb=suburb).all()
		return json.dumps(OLX.serialize_list(olxs))
if __name__ == '__main__':
    app.run()