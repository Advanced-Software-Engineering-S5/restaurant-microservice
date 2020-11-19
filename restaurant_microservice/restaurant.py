from restaurant_microservice.database import db, Restaurant, RestaurantTable
from flask import jsonify, request
from sqlalchemy import exc

def get_restaurants():  
    allrestaurants = db.session.query(Restaurant)
    return [p.to_dict() for p in allrestaurants]

def get_restaurant(restaurant_id):  
    q = Restaurant.query.filter_by(id=restaurant_id).first()
    if q is None:
        return 'Restaurant not found',404
    return q.to_dict()

def get_multiple_restaurants():
    try:
        rest_ids = request.get_json()['restaurant_ids']
        restaurants = Restaurant.query.filter(id.in_(rest_ids)).all()
        return {'restaurants': [r.to_dict() for r in restaurants]}
    except:
        return {}, 500


def get_restaurant_tables(restaurant_id):
    seats = request.args.get('seats', None)
    if seats:
        tables = RestaurantTable.query.filter_by(restaurant_id=restaurant_id, seats=seats)
    else:
        tables = RestaurantTable.query.filter_by(restaurant_id=restaurant_id)
    if tables is None:
        return 'Restaurant not found',404
    response = []
    for t in tables:
        response.append({'table_id' : t.table_id, 'seats' : t.seats})
    m = jsonify({"tables" : response})
    m.status_code = 200
    return m

def create_restaurant():
    body = request.get_json()
    r = Restaurant(**body)
    try:
        db.session.add(r)
        db.session.commit()
    except exc.IntegrityError as e:
        return "A restaurant with the same phone number already exists", 500
    return r.id, 200

def delete_restaurant(restaurant_id):
    q = Restaurant.query.filter_by(id=restaurant_id).first()
    if q is None:
        return 'Restaurant not found',404
    try:
        db.session.delete(q)
        db.session.commit()
    except Exception as e:
        return str(e), 500
    return {}, 200

def edit_restaurant(restaurant_id):
    body = request.get_json()
    tables = body['tables']
    RestaurantTable.query.filter_by(restaurant_id = restaurant_id).delete()
    try:
        db.session.commit()
    except Exception as e:
        return str(e), 500
    i = 1
    for t in tables:
        new_table = RestaurantTable()
        new_table.restaurant_id = int(restaurant_id)
        new_table.table_id = int(t['table_id'])
        new_table.seats = int(t['seats'])
        db.session.add(new_table)
        i += 1
    try:
        db.session.commit()
        return {}, 201
    except Exception as e:
        return str(e), 500