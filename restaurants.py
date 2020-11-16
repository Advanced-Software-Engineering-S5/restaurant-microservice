from flask import request
from database import Restaurant

def get_multiple_restaurants():
    rest_ids = request.get_json()
    