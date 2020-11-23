from os import environ
from restaurant_microservice.background import celery
from restaurant_microservice.database import Restaurant, Review, db
import logging

@celery.task
def average_review_stars():
    """
        Task run periodically in an async manner, used for computing the
        mean review score of every restaurant.
    """
    # get all un-counted reviews
    reviews = Review.query.filter_by(marked=False).join(Restaurant)\
        .with_entities(Review, Restaurant).all()
    logging.info(f"Averaging review stars of {len(reviews)} retrieved reviews..")
    for review, restaurant in reviews:
        # compute running mean of reviews
        restaurant.num_reviews += 1
        restaurant.avg_stars = 1/restaurant.num_reviews * \
            (restaurant.avg_stars * (restaurant.num_reviews-1) + review.stars)
        review.marked = True
    # update rows            
    db.session.commit() 

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Register the average review star task
    sender.add_periodic_task(60.0, average_review_stars.s(), name='average_review_stars')