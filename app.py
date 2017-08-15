from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import OLX


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/post_data', methods=['GET', 'POST'])
def post_data(limit):
	if request.method == "POST":
		if not request.json:
        	abort(400)
		json_dict = request.get_json()
		olx = OLX(**json_dict)
		db.session.add(olx)
        db.session.commit()
        return jsonify({'success': True}), 201

@app.route('/fetch_data/<limit>', methods=['GET', 'POST'])
def post_data(limit):
    if request.method == "GET":
    	olxs = OLX.query.limit(int(limit)).all()
    	return jsonify({'data': olxs})

if __name__ == '__main__':
    app.run()