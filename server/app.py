#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants')
def restaurants():
    restaurant_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    return make_response(
        restaurant_list,
        200
    )

@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response(
            {"error": "Restaurant not found"},
            404
        )
    elif request.method == 'GET':
        return make_response(
            restaurant.to_dict(rules=('pizzas',)),
            200
        )
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response(
            {},
            200
        )

@app.route('/pizzas')
def pizzas():
    pizza_list = [pizza.to_dict() for pizza in Pizza.query.all()]
    return make_response(
        pizza_list,
        200
    )

@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizza():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_restaurant_pizza = RestaurantPizza(
                price = data['price'],
                pizza_id = data['pizza_id'],
                restaurant_id = data['restaurant_id']
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return make_response(
                new_restaurant_pizza.pizza.to_dict(),
                201
            )
        except Exception as e:
            return make_response(
                {"error": "Invalid input"},
                404
            )

if __name__ == '__main__':
    app.run(port=5555, debug=True)
