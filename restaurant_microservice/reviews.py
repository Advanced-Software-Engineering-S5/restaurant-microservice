from restaurant_microservice.database import Review
from flask import request
from restaurant_microservice.database import db, Review
from sqlalchemy import exc

def add_review(restaurant_id):
    """Adds a new review for the restaurant_id
    """
    body = request.get_json()
    r = Review(**body)
    r.restaurant_id = restaurant_id
    try:
        db.session.add(r)
        db.session.commit()
    except exc.IntegrityError as e:
        return "A review of the user to this restaurant already exists", 500
    return {}, 201

def get_restaurant_reviews(restaurant_id, user_id=None):
    """Gets the reviews for the restaurant_id
    """
    if user_id:
        reviews = Review.query.filter_by(restaurant_id=restaurant_id, reviewer_id=int(user_id))
    else:
        reviews = Review.query.filter_by(restaurant_id=restaurant_id)
    return [p.to_dict() for p in reviews], 200

def get_user_reviews(user_id):
    """Gets all the reviews of a single user
    """
    allreviews = Review.query.filter_by(reviewer_id=user_id)
    return [p.to_dict() for p in allreviews], 200