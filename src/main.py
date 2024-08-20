# src/main.py
from src.producer.kafka_producer import FlickrKafkaProducer
from src.consumer.spark_streaming import SparkStreamingConsumer
import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config/app_config.yml')

    api_key = config['flickr']['api_key']
    kafka_topic = config['kafka']['topic']
    kafka_servers = config['kafka']['servers'].split(',')

    producer = FlickrKafkaProducer(api_key, kafka_topic, kafka_servers)
    producer.fetch_and_send(lat=40.7128, lon=-74.0060)  # New York City coordinates
    producer.close()

    consumer = SparkStreamingConsumer(kafka_topic, kafka_servers)
    consumer.process_stream()
