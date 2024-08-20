# src/main.py
import sys
import os

# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.producer.kafka_producer import FlickrKafkaProducer
from src.utils.config import Config
from src.utils.logging_util import setup_logging
from src.consumer.spark_streaming import SparkStreamingConsumer

import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config/app_config.yml')

    api_key = config['flickr']['api_key']
    kafka_topic = config['kafka']['topic']
    kafka_servers = config['kafka']['servers'].split(',')

    producer = FlickrKafkaProducer(api_key, kafka_topic, kafka_servers)
    producer.fetch_and_send(lat=51.91991, lon=4.47991)  # New York City coordinates
    producer.close()

    consumer = SparkStreamingConsumer(kafka_topic, kafka_servers)
    consumer.process_stream()
