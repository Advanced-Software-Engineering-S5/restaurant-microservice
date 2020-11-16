from database import db, Restaurant, Review, RestaurantTable
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

"""def create_restaurant(name, lat, lon, phone, extra_info):
    r = Restaurant(name=name, lat=lat, lon=lon, phone=phone, extra_info=extra_info)
    db.session.add(r)
    db.session.commit()"""

def create_restaurant():
    body = request.get_json()
    r = Restaurant(**body)
    try:
        db.session.add(r)
        db.session.commit()
    except exc.IntegrityError as e:
        return "A restaurant with the same phone number already exists", 500
    return r.id, 200

def edit_restaurant(restaurant_id):
    body = request.get_json()
    tables = body['tables']
    RestaurantTable.query.filter_by(restaurant_id = restaurant_id).delete()
    try:
        db.session.commit()
    except:
        return 'cazzo però', 500
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
    except:
        return 'cazzo però', 500