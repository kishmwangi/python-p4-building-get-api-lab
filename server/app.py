#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = Bakery.query.all()
    return jsonify([{
        'id': bakery.id,
        'name': bakery.name,
        'location': bakery.location
    } for bakery in bakeries])

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if bakery is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    return jsonify({
        'id': bakery.id,
        'name': bakery.name,
        'location': bakery.location,
        'baked_goods': [{
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price
        } for baked_good in bakery.baked_goods]
    })

@app.route('/baked_goods/by_price', methods=['GET'])
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([{
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price
    } for baked_good in baked_goods])

@app.route('/baked_goods/most_expensive', methods=['GET'])
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good is None:
        return make_response(jsonify({'error': 'No baked goods found'}), 404)

    return jsonify({
        'id': baked_good.id,
        'name': baked_good.name,
        'price': baked_good.price
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
