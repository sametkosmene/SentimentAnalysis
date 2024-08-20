# tests/test_kafka_producer.py
import unittest
from src.producer.kafka_producer import FlickrKafkaProducer
from unittest.mock import patch

class TestFlickrKafkaProducer(unittest.TestCase):
    @patch('src.producer.kafka_producer.FlickrAPIClient.get_photos')
    def test_fetch_and_send(self, mock_get_photos):
        mock_get_photos.return_value = {"photos": {"photo": [{"id": "1", "tags": "test"}]}}
        producer = FlickrKafkaProducer(api_key="dummy_api_key", kafka_topic="dummy_topic", kafka_servers=["localhost:9092"])
        producer.fetch_and_send(lat=40.7128, lon=-74.0060)
        producer.close()
