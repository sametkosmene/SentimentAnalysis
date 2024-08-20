from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col

def process_streaming_data(spark):
    """Process streaming data from Kafka."""
    df = (spark.readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", "localhost:9092")
              .option("subscribe", "flickr_topic")
              .load())
    
    df = df.selectExpr("CAST(value AS STRING) as json")
    df = df.select(split(col("json"), ' ').alias("tags"))

    df = df.withColumn("tag", explode(col("tags")))
    df = df.groupBy("tag").count().orderBy("count", ascending=False)

    query = (df.writeStream
                .outputMode("complete")
                .format("console")
                .start())
    
    query.awaitTermination()

if __name__ == "__main__":
    spark = SparkSession.builder.appName("FlickrTagAnalysis").getOrCreate()
    process_streaming_data(spark)
