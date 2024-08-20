# src/consumer/spark_streaming.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, desc, dense_rank
from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark.sql.window import Window

class SparkStreamingConsumer:
    def __init__(self, kafka_topic, kafka_servers):
        self.spark = SparkSession.builder \
            .appName("FlickrSentimentAnalysis") \
            .getOrCreate()
        self.kafka_topic = kafka_topic
        self.kafka_servers = kafka_servers

    def process_stream(self):
        schema = StructType() \
            .add("id", StringType()) \
            .add("title", StringType()) \
            .add("tags", StringType()) \
            .add("owner", StringType()) \
            .add("lat", StringType()) \
            .add("lon", StringType())

        # Reading from Kafka
        df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_servers) \
            .option("subscribe", self.kafka_topic) \
            .load() \
            .selectExpr("CAST(value AS STRING)")

        # Parsing JSON data
        df = df.withColumn("data", from_json(col("value"), schema)).select("data.*")

        # Splitting tags into separate rows
        df = df.withColumn("tag", explode(split(col("tags"), " ")))

        # Counting the tags for each (latitude, longitude) pair
        df = df.groupBy("lat", "lon", "tag").count()

        # Selecting the top 10 tags per (lat, lon) pair
        window = Window.partitionBy("lat", "lon").orderBy(desc("count"))
        windowed_df = df.withColumn("rank", dense_rank().over(window)) \
                        .filter(col("rank") <= 10) \
                        .drop("rank")

        # Writing the results to console in real-time
        query = windowed_df.writeStream \
            .outputMode("complete") \
            .format("console") \
            .start()

        query.awaitTermination()

if __name__ == "__main__":
    kafka_topic = "flickr_photos"
    kafka_servers = ["localhost:9092"]

    consumer = SparkStreamingConsumer(kafka_topic, kafka_servers)
    consumer.process_stream()
