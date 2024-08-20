# tests/test_flickr_api_client.py
import unittest
from src.producer.flickr_api_client import FlickrAPIClient

class TestFlickrAPIClient(unittest.TestCase):
    def test_get_photos(self):
        client = FlickrAPIClient(api_key="dummy_api_key")
        response = client.get_photos(lat=40.7128, lon=-74.0060)
        self.assertTrue('photos' in response)
