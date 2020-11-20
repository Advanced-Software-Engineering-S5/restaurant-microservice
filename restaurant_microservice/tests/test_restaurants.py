from restaurant_microservice.database import RestaurantTable, db, Restaurant
import unittest, logging
from restaurant_microservice.app import create_app

class TestRestaurants(unittest.TestCase):
    def setUp(self) -> None:
        self.restaurant_data = {'name': 'Mensa martiri', 
                    'lat': 4.12345,
                    'lon': 5.67890,
                    'phone': '3333333333',
                    'extra_info': 'Rigatoni dorati h24, cucina povera'}
        table_2 = {'table_id':2, 'restaurant_id':1, 'seats':6}
        self.app = create_app(dbfile='sqlite:///:memory:')
        with self.app.app_context():
            db.session.add(Restaurant(**self.restaurant_data))
            db.session.add(RestaurantTable(**table_2))
            db.session.commit()


    def test_get_restaurants(self):
        with self.app.test_client() as client:
            response = client.get('/restaurants')
            self.assertEqual(len(response.get_json()), 2)


    def test_get_restaurant(self):
        with self.app.test_client() as client:
            response = client.get('/restaurants/1')
            self.assertEqual(response.status_code, 200)
            response = client.get('/restaurants/100')
            self.assertEqual(response.status_code, 404)


    def test_get_multiple_restaurant(self):
        with self.app.test_client() as client:
            data = {"restaurant_ids":[1, 2]}
            response = client.post("/restaurants", json=data)
            self.assertEqual(response.status_code, 200)
            response = client.post("/restaurants")
            self.assertEqual(response.status_code, 400)


    def test_get_restaurant_tables(self):
        with self.app.test_client() as client:
            response = client.get("/restaurants/tables/1")
            self.assertEqual(response.status_code, 200)
            response = client.get("/restaurants/tables/1?seats=4")
            self.assertEqual(response.status_code, 200)
            response = client.get("/restaurants/tables/100")
            self.assertEqual(response.status_code, 404)


    def test_create_restaurant(self):
        with self.app.test_client() as client:
            response = client.post("/restaurants/new", json=self.restaurant_data)
            self.assertEqual(response.status_code, 500)
            a = self.restaurant_data.copy()
            a['phone'] = '322222222'
            response = client.post("/restaurants/new", json=a)
            self.assertEqual(response.status_code, 200)


    def test_delete_restaurant(self):
        with self.app.test_client() as client:
            response = client.delete("/restaurants/2")
            self.assertEqual(response.status_code, 200)
            response = client.delete("/restaurants/2")
            self.assertEqual(response.status_code, 404)

    
    def test_edit_restaurant(self):
        with self.app.test_client() as client:
            data = {
                "phone":"222222222",
                "tables":[
                    {"table_id":1, "seats":4},
                    {"table_id":2, "seats":8}
                ]
            }
            response = client.put("/restaurants/1", json=data)
            self.assertEqual(response.status_code, 201)
            # response = client.put("/restaurants/update/10", json=data)
            # self.assertEqual(response.status_code, 500)