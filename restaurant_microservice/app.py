# from database import Restaurant
import datetime
from datetime import time
from restaurant_microservice.database import RestaurantTable, db, Restaurant
import connexion, logging

db_session = None

logging.basicConfig(level=logging.INFO)
def create_app(dbfile='sqlite:///restaurant_gooutsafe.db'):
    app = connexion.App(__name__)
    app.add_api('swagger.yml')
    app = app.app
    # app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    # app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['SQLALCHEMY_DATABASE_URI'] = dbfile
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # celery config
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

    db.init_app(app)
    db.create_all(app=app)

    with app.app_context():
        q = db.session.query(Restaurant).filter(Restaurant.id == 1)
        restaurant = q.first()
        if restaurant is None:
            restaurant = Restaurant()
            restaurant.name = 'Trial Restaurant'
            restaurant.avg_stay_time = time(hour=1)
            restaurant.likes = 42
            restaurant.phone = '555123456'
            restaurant.lat = 43.720586
            restaurant.lon = 10.408347
            restaurant.avg_stay_time = datetime.time(1, 30)
            db.session.add(restaurant)
            db.session.commit()
        
        q = db.session.query(RestaurantTable).filter(RestaurantTable.restaurant == restaurant)
        restaurant_table = q.first()
        if restaurant_table is None:
            restaurant_table = RestaurantTable(table_id=1, restaurant=restaurant, seats=4)
            db.session.add(restaurant_table)
            db.session.commit()

    # set the WSGI application callable to allow using uWSGI:
    # uwsgi --http :8080 -w app
    return app

# @application.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080)