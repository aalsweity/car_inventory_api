from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Car Brand': 'Delorean',
            'Car Model': 'DMC12',
            'Car Transmission' : 'Automatic',
            'Car Year' : '1983'
            }
    
@api.route('/inventory', methods = ['POST'])
@token_required
def create_car(current_user_token):
    car_brand = request.json['car_brand']
    car_model = request.json['car_model']
    car_transmission = request.json['car_transmission']
    car_year = request.json['car_year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(car_brand, car_model, car_transmission, car_year, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    car = Car.query.get(id) 
    car.car_brand = request.json['car_brand']
    car.car_model = request.json['car_model']
    car.car_transmission = request.json['car_transmission']
    car.car_year = request.json['car_year']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)