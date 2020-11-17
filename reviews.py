from database import Review
from flask import request
from database import db, Review
from sqlalchemy import exc

def add_review(restaurant_id):
    body = request.get_json()
    r = Review(**body)
    r.restaurant_id = restaurant_id
    try:
        db.session.add(r)
        db.session.commit()
    except exc.IntegrityError as e:
        return "A review of the user to this restaurant already exists", 500
    return {}, 201

def get_restaurant_reviews(restaurant_id):
    allreviews = Review.query.filter_by(restaurant_id=restaurant_id)
    return [p.to_dict() for p in allreviews]

def get_user_reviews(user_id):
    allreviews = Review.query.filter_by(reviewer_id=user_id)
    return [p.to_dict() for p in allreviews]