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
    'db': 'olx_v1',
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
	q = db.session.query(OLX).filter(OLX.phone_number.startswith("("))
	for row in q:
		row.phone_number = row.phone_number.replace("(","").replace(")", "").replace(" ","").strip()
		row.phone_number = "55{0}".format(row.phone_number)
		print(row.phone_number)
		db.session.add(row)
		db.session.commit()
	return "OLX APP"


@app.route('/post_data', methods=['GET', 'POST'])
def post_data():
	if request.method == "POST":
		if not request.json:
			abort(400)
		json_dict = request.get_json()
		# adcode_exist = OLX.query.filter_by(adcode=json_dict["adcode"]).first()
		# # adcode_exist = db.session.query(OLX).filter(OLX.adcode == json_dict["adcode"]).first()
		# if adcode_exist:
		# 	print("Already Exist")
		# 	return "Already Exist"
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
			olxs = db.session.query(OLX).filter(OLX.phone_number.ilike(phone)).filter(OLX.adcode.ilike(adcode))
		elif phone:
			olxs = db.session.query(OLX).filter(OLX.phone_number.ilike(phone))
		elif adcode:
			olxs = db.session.query(OLX).filter(OLX.adcode.ilike(adcode))

		if city and suburb:
			olxs = db.session.query(OLX).filter(OLX.city.ilike(city)).filter(OLX.suburb.ilike(suburb))
		elif city:
			olxs = db.session.query(OLX).filter(OLX.city.ilike(city))
		elif suburb:
			olxs = db.session.query(OLX).filter(OLX.suburb.ilike(suburb))
		if olxs:
			olxs = olxs.distinct(OLX.adcode)
			olxs = olxs.all()
		return json.dumps(OLX.serialize_list(olxs))



@app.route('/download/', methods=['GET'])
def csv_download():
	categ = request.args.get('categ', None)
	subcateg = request.args.get('subcateg', None)
	suburb = request.args.get('suburb', None)
	city = request.args.get('city', None)
	fields = json.loads(request.args.get('fields', ""))
	limit = request.args.get('limit', 10000)
	offset = request.args.get('offset', 0)

	results = []
	olxs = []

	if not fields:
		fields = ['title', 'phone_number']

	if request.method == "GET":

		if city and city != "null" and suburb and suburb != "null":
			olxs = db.session.query(OLX).filter(OLX.city.ilike(city)).filter(OLX.suburb.ilike(suburb))
		elif city != "null":
			olxs = db.session.query(OLX).filter(OLX.city.ilike(city))

		elif suburb != "null":
			olxs = db.session.query(OLX).filter(OLX.suburb.ilike(suburb))

		if categ != "null" and olxs and subcateg != "null":
			olxs = olxs.filter(OLX.main_category.ilike(categ)).filter(OLX.sub_category.ilike(subcateg))
		elif olxs and categ != "null":
			olxs = olxs.filter(OLX.main_category.ilike(categ))
		elif olxs and subcateg != "null":
			olxs = olxs.filter(OLX.sub_category.ilike(subcateg))

		if limit:
			olxs = olxs.limit(int(limit))

		if offset:
			olxs = olxs.offset(int(offset))

		dat = olxs.all()

		dat = OLX.serialize_list(dat)
		for d in dat:
			obj = {}
			for f in fields:
				 obj[f] =  d[f]
			if obj:
				results.append(obj)

		data = results

		if data:
			si = StringIO()
			dict_writer = csv.DictWriter(si, data[0].keys())
			dict_writer.writeheader()
			dict_writer.writerows(data)
			output = make_response(si.getvalue())
			output.headers["Content-Disposition"] = "attachment; filename={0}.csv".format(list(data[0].keys())[0])
			output.headers["Content-type"] = "text/csv"
			return output
		return jsonify({'message': "No Data Found"}), 200


@app.route('/download_page/', methods=['GET'])
def download_page():
	if request.method == "GET":
		return render_template("download_page2.html")


@app.route("/city_list/",  methods=['GET'])
def city_list():
	if request.method == "GET":
		cities = db.session.query(OLX.city.distinct().label("city"))
		city_list = sorted([row.city for row in cities.all() if row.city])
		return json.dumps(city_list)


@app.route("/suburb_list/",  methods=['GET'])
def suburb_list():
	if request.method == "GET":
		query = request.args.get('query')

		suburb = db.session.query(OLX.suburb.distinct().label("suburb")).filter(OLX.city.startswith(query)).all()
		suburb_list = [row.suburb for row in suburb if row.suburb]
		suburbs = sorted([i for i in suburb_list if i])
		suburbs = list(set(suburb_list))
		return json.dumps(suburbs)


@app.route("/categ_list/",  methods=['GET'])
def categ_list():
	if request.method == "GET":
		main_category = db.session.query(OLX.main_category.distinct().label("main_category"))
		category_list = sorted([row.main_category for row in main_category.all() if row.main_category ])
		return json.dumps(category_list)


@app.route("/subcateg_list/",  methods=['GET'])
def subcateg_list():
	if request.method == "GET":
		query = request.args.get('query')
		sub_category = db.session.query(OLX.sub_category.distinct().label("sub_category")).filter(OLX.main_category.startswith(query)).all()
		sub_category_list = [row.sub_category for row in sub_category]
		sub_categories = sorted([i for i in sub_category_list if i])
		sub_categories = list(set(sub_categories))

		return json.dumps(sub_categories)


if __name__ == '__main__':
    app.run()