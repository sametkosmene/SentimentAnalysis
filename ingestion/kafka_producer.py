from kafka import KafkaProducer
import json
import requests
from config.kafka_config import KAFKA_TOPIC, KAFKA_BROKER

def fetch_flickr_data(area_name, page=1, per_page=100):
    """Fetch data from Flickr API."""
    url = f"https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=YOUR_FLICKR_API_KEY&tags={area_name}&format=json&nojsoncallback=1&per_page={per_page}&page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def send_to_kafka(data, producer, topic):
    """Send data to Kafka topic."""
    for item in data:
        producer.send(topic, json.dumps(item).encode('utf-8'))

def main():
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    area_name = 'YOUR_AREA_NAME'
    page = 1
    
    while True:
        data = fetch_flickr_data(area_name, page)
        photos = data.get('photos', {}).get('photo', [])
        if not photos:
            break
        send_to_kafka(photos, producer, KAFKA_TOPIC)
        print(f"Sent page {page} to Kafka")
        page += 1

if __name__ == "__main__":
    main()
