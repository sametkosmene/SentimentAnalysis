import unittest
from pyspark.sql import SparkSession
from processing.spark_streaming import process_stream

class TestSparkStreaming(unittest.TestCase):

    def setUp(self):
        self.spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()
        self.data = [
            ("LA", "sunset beach"),
            ("LA", "sunset mountains"),
            ("NYC", "sunset city"),
            ("NYC", "happy times")
        ]
        self.df = self.spark.createDataFrame(self.data, ["area", "tags"])

    def test_process_stream(self):
        processed_df = process_stream(self.df)
        result = processed_df.collect()

        expected_result = [
            ("LA", "sunset", 2),
            ("NYC", "sunset", 1),
            ("NYC", "happy", 1)
        ]
        
        self.assertEqual(len(result), len(expected_result))

        for row in expected_result:
            self.assertIn(row, result)

    def tearDown(self):
        self.spark.stop()

if __name__ == '__main__':
    unittest.main()
