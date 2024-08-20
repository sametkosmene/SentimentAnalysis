import unittest
from unittest.mock import patch, MagicMock
from ingestion.kafka_producer import FlickrKafkaProducer

class TestFlickrKafkaProducer(unittest.TestCase):

    @patch('ingestion.kafka_producer.KafkaProducer')
    @patch('ingestion.kafka_producer.FlickrAPI')
    def test_produce_messages(self, MockFlickrAPI, MockKafkaProducer):
        mock_producer = MagicMock()
        MockKafkaProducer.return_value = mock_producer

        mock_flickr_api = MagicMock()
        MockFlickrAPI.return_value = mock_flickr_api
        mock_flickr_api.search_photos.return_value = [{"tags": "sunset beach", "area": "LA"}]

        producer = FlickrKafkaProducer(kafka_topic="flickr_topic", kafka_broker="localhost:9092")
        producer.produce_messages()

        # Check if the message was sent to Kafka
        self.assertTrue(mock_producer.send.called)
        mock_producer.send.assert_called_with("flickr_topic", b'{"tags": "sunset beach", "area": "LA"}')

if __name__ == '__main__':
    unittest.main()
