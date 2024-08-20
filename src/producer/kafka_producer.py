# src/producer/kafka_producer.py
from kafka import KafkaProducer
import json
from .flickr_api_client import FlickrAPIClient

class FlickrKafkaProducer:
    def __init__(self, api_key, kafka_topic, kafka_servers):
        self.client = FlickrAPIClient(api_key)
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.kafka_topic = kafka_topic

    def fetch_and_send(self, lat, lon, tags=None):
        photos = self.client.get_photos(lat, lon, tags)
        for photo in photos['photos']['photo']:
            self.producer.send(self.kafka_topic, photo)

    def close(self):
        self.producer.close()
