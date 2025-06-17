from kafka import KafkaProducer
import json
import time
import uuid
import os
import random

# Initialize Kafka producer with JSON serialization of messages
producer = KafkaProducer(
    bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],  # Kafka broker address
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize dict to JSON bytes
)

def create_order():
    '''
    Continuously produces order events for restaurant "restro_2"
    with a fixed countdown of 120 seconds.

    Each order has a unique UUID as order_id and status "created".
    Sends one order every 10 seconds to the Kafka topic 'orders'.
    '''
    restaurants = ["restro_1", "restro_2"]
    while True:
        order = {
            "order_id": str(uuid.uuid4()),
            "restaurant_id": random.choice(restaurants),
            "countdown": 120,
            "status": "created"
        }
        print(f"Producing order: {order}")
        producer.send('orders', value=order)
        time.sleep(5)

if __name__ == "__main__":
    # Start producing orders
    create_order()
