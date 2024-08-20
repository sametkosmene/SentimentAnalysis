#!/bin/bash

# Run Spark Streaming Job

echo "Starting Spark Streaming Job..."

# Define Spark master (adjust as per your Spark cluster setup)
SPARK_MASTER="local[*]"  # Use "spark://master-url:7077" for cluster

# Define the path to your Spark application
SPARK_APP="processing/spark_streaming.py"

# Run the Spark application
spark-submit --master $SPARK_MASTER $SPARK_APP

echo "Spark Streaming Job has started."
