#!/bin/bash

# Run Kafka Producer for Flickr Data Ingestion

echo "Starting Kafka Producer for Flickr Data Ingestion..."

# Navigate to the ingestion directory
cd ingestion

# Run the Kafka Producer
python3 kafka_producer.py

echo "Kafka Producer has started. Ingesting data into Kafka topic..."
