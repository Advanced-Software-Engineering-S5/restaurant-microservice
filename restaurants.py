from flask import request
from database import Restaurant

def get_multiple_restaurants():
    try:
        rest_ids = request.get_json()['restaurant_ids']
        restaurants = Restaurant.query.filter(id.in_(rest_ids)).all()
        return {'restaurants': [r.to_dict() for r in restaurants]}
    except:
        return {}, 500