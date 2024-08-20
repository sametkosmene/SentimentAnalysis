# src/main.py
import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col
from src.producer.kafka_producer import FlickrKafkaProducer
from src.utils.config import Config
from src.utils.logging_util import setup_logging
#from src.consumer.spark_streaming import SparkStreamingConsumer
from mainconfig import FLICKR_API_KEY, KAFKA_SERVER, KAFKA_TOPIC

def setup_spark_streaming(kafka_bootstrap_servers, kafka_topic):
    """Set up and start Spark Streaming job."""
    spark = SparkSession.builder \
        .appName("FlickrSentimentAnalysis") \
        .getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    df = df.selectExpr("CAST(value AS STRING)")
    df = df.withColumn("tags", split(col("value"), ","))
    df = df.withColumn("tag", explode(col("tags")))

    tag_counts = df.groupBy("tag").count()

    query = tag_counts \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()

def main():
    # Print the current working directory and PYTHONPATH for debugging
    print("Current working directory:", os.getcwd())
    print("Python path:", sys.path)

    ## Load configurations
    #app_config = Config('config/app_config.yml')
    #kafka_config = Config('config/kafka_config.yml')

    # Set up logging
    setup_logging(log_file="logs/app.log")

    # Initialize Kafka producer and consumer
    kafka_topic = KAFKA_TOPIC
    kafka_servers = KAFKA_SERVER
    api_key = FLICKR_API_KEY

    # Create instances of the producer and consumer
    producer = FlickrKafkaProducer(api_key, kafka_topic, kafka_servers)
    # consumer = SparkStreamingConsumer(kafka_topic, kafka_servers)
    setup_spark_streaming(kafka_servers, kafka_topic)

    # Example usage: Fetch photos and send to Kafka
    # You can adjust latitude and longitude as needed
    producer.fetch_and_send(lat="51.91991", lon="4.47991")

    ## Process the stream to analyze sentiments
    #consumer.process_stream()

if __name__ == "__main__":
    main()
