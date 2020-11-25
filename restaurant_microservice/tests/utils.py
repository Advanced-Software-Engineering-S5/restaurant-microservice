from restaurant_microservice.database import Restaurant, db
from datetime import datetime, timedelta, time
import random
from flask import Flask
from werkzeug.security import generate_password_hash
import connexion
import os

def create_app_for_test():
    # creates app using in-memory sqlite db for testing purposes
    app = connexion.App(__name__)
    app.add_api('../swagger.yml')
    app = app.app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'

    # celery config
    app.config['CELERY_BROKER_URL'] = f"redis://{os.environ.get('GOS_REDIS')}/{os.environ.get('CELERY_DB_NUM')}"
    app.config['CELERY_RESULT_BACKEND'] = f"redis://{os.environ.get('GOS_REDIS')}/{os.environ.get('CELERY_DB_NUM')}"

    db.init_app(app)
    db.create_all(app=app)

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    return app

def add_random_restaurants(n_places: int, app: Flask):
    counter = 1
    with app.app_context():
        rests = []
        for i in range(n_places):
            stay_time = time(hour=1)
            res = Restaurant(name=f'test_rest_{i}', lat = 42.111,lon = 11.111, phone = '343493490'+str(counter),
             extra_info = '', avg_stay_time=stay_time)
            rests.append(res)
            counter += 1
        db.session.add_all(rests)
        db.session.commit()