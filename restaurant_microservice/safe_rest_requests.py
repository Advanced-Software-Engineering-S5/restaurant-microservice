import requests
import logging

def get(url: str, *args, **kwargs):
    try: # TODO: timeouts
        return requests.get(url, *args, **kwargs)
    except Exception as e:
        logging.error(f"Error in GET request to endpoint {url} with message: {e}")
        return None
