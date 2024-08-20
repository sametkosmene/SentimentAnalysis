# tests/test_spark_streaming.py
import unittest
from src.consumer.spark_streaming import SparkStreamingConsumer

class TestSparkStreamingConsumer(unittest.TestCase):
    def test_process_stream(self):
        consumer = SparkStreamingConsumer(kafka_topic="dummy_topic", kafka_servers=["localhost:9092"])
        # Since this is a streaming application, we can only test if it starts correctly.
        try:
            consumer.process_stream()
        except Exception as e:
            self.fail(f"process_stream() raised {e} unexpectedly!")
