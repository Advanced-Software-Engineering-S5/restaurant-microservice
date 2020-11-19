import sys
import unittest, logging
from restaurant_microservice.app import create_app

class TestRestaurants(unittest.TestCase):

    def create_app(self):
        self.app = create_app(":memory:")
        self.app.config['TESTING'] = True
        # Default port is 5000
        self.app.config['LIVESERVER_IP'] = "0.0.0.0"
        self.app.config['LIVESERVER_PORT'] = 5000
        # Default timeout is 5 seconds
        self.app.config['LIVESERVER_TIMEOUT'] = 10
        return self.app

    def test_multiple_restaurant_ids(self):
        app = create_app(dbfile='sqlite:///:memory:')
        app = None
        with app.test_client() as client:
            a = str(client.get('/'))
            print(a)
        return True

    def test_multiple_restaurant_ids_empty(self):
        pass