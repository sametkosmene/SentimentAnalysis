# src/consumer/spark_streaming.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, count
from pyspark.sql.types import StringType

def process_stream():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("FlickrSentimentAnalysis") \
        .getOrCreate()

    # Kafka configurations
    kafka_bootstrap_servers = "localhost:9092"
    kafka_topic = "flickr_photos"

    # Read streaming data from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    # Extract the message value
    df = df.selectExpr("CAST(value AS STRING)")

    # Split tags and count occurrences
    df = df.withColumn("tags", split(col("value"), ","))
    df = df.withColumn("tag", explode(col("tags")))

    # Group by tag and count occurrences
    tag_counts = df.groupBy("tag").count()

    # Write the results to the console (or you can write to a file, database, etc.)
    query = tag_counts \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    # Await termination
    query.awaitTermination()

if __name__ == "__main__":
    process_stream()
