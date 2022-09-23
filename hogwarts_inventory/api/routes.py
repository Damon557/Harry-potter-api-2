from flask import Blueprint, request, jsonify
from hogwarts_inventory.helper import token_required
from hogwarts_inventory.models import db, Wand, wand_schema, wands_schema

api = Blueprint('api', __name__, url_prefix = '/api')



@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'name': 'lando'}



@api.route('/hogwarts', methods = ['POST'])
@token_required
def create_hogwarts(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    spell_strenght = request.json['spell_strenght']
    casting_time = request.json['casting_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    wand = wands(name, description, price, spell_strenght, casting_time, max_speed, dimensions, weight, cost_of_production, series, user_token = user_token)

    db.session.add(wand)
    db.session.commit()

    response =wand_schema.dump(wand)
    return jsonify(response)



@api.route( 'wands/<id>', methods = ['GET'])
@token_required
def get_wand(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
       wand =wand.query.get(id)
       response =wand_schema.dump(wand)
       return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route(' wands', methods = ['GET']) 
@token_required
def wands(current_user_token):
    owner = current_user_token.token 
    wands =Wand.query.filter_by(user_token = owner).all()
    response = wands_schema.dump(wands)
    return jsonify(response)


@api.route(' wands/<id>', methods = ['POST', 'PUT'])
@token_required
def update_drone(current_user_token, id):
   wand =wands.query.get(id)    
   wand.name = request.json['name']
   wand.description = request.json['description']
   wand.price = request.json['price']
   wand.camera_quality = request.json['spell_strenght']
   wand.flight_time = request.json['casting_time']
   wand.max_speed = request.json['max_speed']
   wand.dimensions = request.json['dimensions']
   wand.weight = request.json['weight']
   wand.cost_of_production = request.json['cost_of_production']
   wand.series = request.json['series']
   wand.user_token = current_user_token.token
   
   db.session.commit()
   response =wand_schema.dump(wand)
   return jsonify(response)


@api.route( 'wands/<id>', methods = ["DELETE"])
@token_required
def delete_wand(current_user_token, id):
   wand =wand.query.get(id)
   db.session.delete(wand)
   db.session.commit()
   response =wand_schema.dump(wand)
   return jsonify(response)