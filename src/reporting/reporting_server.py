# src/reporting/reporting_server.py

from flask import Flask, jsonify
import os
import pandas as pd

app = Flask(__name__)

@app.route('/report', methods=['GET'])
def get_report():
    try:
        # Load the latest tag counts from the CSV file
        csv_files = sorted([f for f in os.listdir('output/tag_counts') if f.endswith('.csv')], reverse=True)
        if not csv_files:
            return jsonify({"error": "No report available"}), 404
        
        latest_file = csv_files[0]
        df = pd.read_csv(os.path.join('output/tag_counts', latest_file))
        
        # Convert the DataFrame to a dictionary
        report = df.to_dict(orient='records')
        return jsonify(report)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
