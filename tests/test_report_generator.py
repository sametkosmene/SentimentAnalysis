import unittest
from unittest.mock import patch, MagicMock
from reporting.report_generator import generate_report

class TestReportGenerator(unittest.TestCase):

    @patch('reporting.report_generator.snowflake.connector.connect')
    def test_generate_report(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [
            ("LA", "sunset", 20),
            ("NYC", "happy", 15)
        ]

        result = generate_report()
        
        expected_result = [
            {"area": "LA", "tag": "sunset", "count": 20},
            {"area": "NYC", "tag": "happy", "count": 15}
        ]

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
