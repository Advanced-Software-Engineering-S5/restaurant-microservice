from restaurant_microservice.database import RestaurantTable, db, Restaurant
import unittest
from restaurant_microservice.app import create_app

class TestReviews(unittest.TestCase):
    def setUp(self) -> None:
        self.review = {'reviewer_id':1,
            'stars':3}
        self.app = create_app(dbfile='sqlite:///:memory:')
        with self.app.app_context():
            #db.session.add(Restaurant(**self.restaurant_data))
            #db.session.add(RestaurantTable(**table_2))
            db.session.commit()

    
    def test_get_reviews_restaurant(self):
        with self.app.test_client() as client:
            response = client.get("/reviews/1")
            self.assertEqual(response.status_code, 200)

    def test_get_reviews_user(self):
        with self.app.test_client() as client:
            response = client.get("/reviews/user/1")
            self.assertEqual(response.status_code, 200)

    def test_add_review(self):
        with self.app.test_client() as client:
            response = client.post("/reviews/1", json=self.review)
            self.assertEqual(response.status_code, 201)
            response = client.post("/reviews/1", json=self.review)
            self.assertEqual(response.status_code, 500)