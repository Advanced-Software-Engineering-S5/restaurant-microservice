import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(100))
    lat = db.Column(db.Float) # restaurant latitude
    lon = db.Column(db.Float) # restaurant longitude
    phone = db.Column(db.Text(20), unique=True)
    extra_info = db.Column(db.Text(300)) # restaurant infos (menu, ecc.)
    avg_stay_time = db.Column(db.Time, default=time(hour=1))
    avg_stars = db.Column(db.Float, default=0.0)
    num_reviews = db.Column(db.Integer, default=0)

    #One to one relationship
    # operator = db.relationship("User", back_populates="restaurant", uselist=False)

    #One to many relationship
    # reservations = db.relationship("Reservation", back_populates="restaurant")

    #One to many relationship
    tables = db.relationship("RestaurantTable", back_populates="restaurant")

    def to_dict(self):
        c = {}
        for column in self.__table__.columns:
            a = getattr(self, column.name)
            if isinstance(a, (datetime, time)):
                c[column.name] = str(a.isoformat())
            else:
                c[column.name] = a
        return c
        


class RestaurantTable(db.Model):
    __tablename__ = 'restaurant_table'
    table_id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    
    restaurant = db.relationship('Restaurant', back_populates="tables")
    seats = db.Column(db.Integer, default=False)

    def to_dict(self):
        return {column.name:getattr(self, column.name) for column in self.__table__.columns}


class Review(db.Model):
    __tablename__ = 'review'

    reviewer_id = db.Column(db.Integer, primary_key=True)
    # reviewer = db.relationship('User', foreign_keys='Review.reviewer_id')

    stars = db.Column(db.Integer)
    text_review = db.Column(db.Text(180), nullable=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), primary_key=True)
    restaurant = db.relationship('Restaurant')

    marked = db.Column(db.Boolean, default=False)  # True iff it has been counted in Restaurant.likes

    def to_dict(self):
        return {column.name:getattr(self, column.name) for column in self.__table__.columns}


