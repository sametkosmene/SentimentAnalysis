# src/producer/flickr_api_client.py
import requests

class FlickrAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.flickr.com/services/rest/"

    def get_photos(self, lat, lon, tags=None, page=1, per_page=100):
        params = {
            'method': 'flickr.photos.search',
            'api_key': self.api_key,
            'lat': lat,
            'lon': lon,
            'radius': 5,
            'format': 'json',
            'nojsoncallback': 1,
            'page': page,
            'per_page': per_page,
            'extras': 'tags'
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
