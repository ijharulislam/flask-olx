 # -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import os
import json

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import csv
from flask import make_response


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
    return "OLX APP"


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
	adcode = request.args.get('adcode', None)
	suburb = request.args.get('suburb', None)
	city = request.args.get('city', None)
	query_param = request.args.get('query_param', None)


	if request.method == "GET":
		olxs = []
		if phone and adcode:
			olxs = OLX.query.filter_by(phone_number=phone).filter_by(adcode=adcode).all()
		elif phone:
			olxs = OLX.query.filter_by(phone_number=phone).all()
		elif adcode:
			olxs = OLX.query.filter_by(adcode=adcode).all()

		if city and suburb:
			olxs = OLX.query.filter_by(city=city).filter_by(suburb=suburb).all()
		elif city:
			olxs = OLX.query.filter_by(city=city).all()
		elif suburb:
			olxs = OLX.query.filter_by(suburb=suburb).all()

		if query_param:
			field = query_param.split("__")[0]
			param = query_param.split("__")[1]
			olxs = OLX.query.filter_by(field=param).all()

		return json.dumps(OLX.serialize_list(olxs))



@app.route('/download/', methods=['GET'])
def csv_download():
	phone = request.args.get('phone', None)
	adcode = request.args.get('adcode', None)
	suburb = request.args.get('suburb', None)
	city = request.args.get('city', None)
	if request.method == "GET":
		olxs = []
		if phone and adcode:
			olxs = OLX.query.filter_by(phone_number=phone).filter_by(adcode=adcode).all()
		elif phone:
			olxs = OLX.query.filter_by(phone_number=phone).all()
		elif adcode:
			olxs = OLX.query.filter_by(adcode=adcode).all()

		if city and suburb:
			olxs = OLX.query.filter_by(city=city).filter_by(suburb=suburb).all()
		elif city:
			olxs = OLX.query.filter_by(city=city).all()
		elif suburb:
			olxs = OLX.query.filter_by(suburb=suburb).all()
		data = OLX.serialize_list(olxs)
		si = StringIO()
		dict_writer = csv.DictWriter(si, data[0].keys())
		dict_writer.writeheader()
		dict_writer.writerows(data)
		output = make_response(si.getvalue())
		output.headers["Content-Disposition"] = "attachment; filename=olx.csv"
		output.headers["Content-type"] = "text/csv"
		return output


@app.route('/download_page/', methods=['GET'])
def download_page():
	if request.method == "GET":
		return render_template("download_page.html")


@app.route("/city_list/",  methods=['GET'])
def city_list():
	if request.method == "GET":
		query = request.args.get('query', None)
		if query:
			olxs = OLX.query.filter(OLX.city.startswith(query)).all()
			data = OLX.serialize_list(olxs)
			city_list = []
			for c in data:
				if c["city"] not in city_list:
					city_list.append(c["city"])
			return json.dumps(city_list)
		else:
			cities = db.session.query(OLX.city.distinct().label("city"))
			city_list = [row.city for row in cities.all() if row.city != None]
			return json.dumps(city_list)


@app.route("/suburb_list/",  methods=['GET'])
def suburb_list():
	if request.method == "GET":
		query = request.args.get('query', [])
		query = json.loads(query)
		print(query)
		suburbs = []
		for q in query:
			suburb = db.session.query(OLX.suburb.distinct().label("suburb")).filter(OLX.city.startswith(q)).all()
			suburbs + [row.suburb for row in suburb]
		return json.dumps(suburbs)

if __name__ == '__main__':
    app.run()