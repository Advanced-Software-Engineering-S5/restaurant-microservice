from restaurant_microservice.database import db, Restaurant, Review
import unittest
from restaurant_microservice.tests.utils import create_app_for_test, add_random_restaurants
from restaurant_microservice.background import make_celery
from celery.contrib.testing.worker import start_worker
from restaurant_microservice.ratings_task import average_review_stars
import random

app = create_app_for_test()
class TestReviews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # start celery worker with test app context and in-memory context 
        celery_app = make_celery(app)
        cls.celery_worker = start_worker(celery_app, perform_ping_check=False)
        # spawn celery worker
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # kill celery worker when tests are done
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self) -> None:
        db.create_all(app=app)
        self.review = {'reviewer_id':1,
            'stars':3}

    def tearDown(self):
        db.drop_all(app=app)
    
    def test_get_reviews_restaurant(self):
        with app.test_client() as client:
            response = client.get("/reviews/1")
            self.assertEqual(response.status_code, 200)
            response = client.get("/reviews/1?user_id=1")
            self.assertEqual(response.status_code, 200)

    def test_get_reviews_user(self):
        with app.test_client() as client:
            response = client.get("/reviews/user/1")
            self.assertEqual(response.status_code, 200)

    def test_add_review(self):
        with app.test_client() as client:
            response = client.post("/reviews/1", json=self.review)
            self.assertEqual(response.status_code, 201)
            response = client.post("/reviews/1", json=self.review)
            self.assertEqual(response.status_code, 500)

    def test_celery_review_update(self):
        with app.app_context():
            # user submits a review 
            stars = random.randint(1, 5)
            add_random_restaurants(1, app)
            rest = Restaurant.query.filter_by(name='test_rest_0').first().to_dict()
            review = Review(reviewer_id=64, stars=stars, restaurant_id=rest['id'])
            db.session.add(review)
            db.session.commit()
            # compute mean (wait for celery worker to be done)
            average_review_stars.delay().get()
            # makes sure it checks out
            rest = Restaurant.query.filter_by(id=rest['id']).first()
            self.assertEqual(rest.avg_stars, stars)
            self.assertEqual(rest.num_reviews, 1) 