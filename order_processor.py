from kafka import KafkaConsumer
import json
import threading
import time
import os

# Dictionary to store current active orders grouped by restaurant_id
orders_by_restaurant = {}

def countdown_worker(order):
    '''
    Background worker function to handle the countdown timer
    for a single order. It decreases the countdown every second
    and removes the order from orders_by_restaurant once the timer
    reaches zero.
    
    Parameters:
    - order: dict containing order details including restaurant_id,
      order_id, and countdown time in seconds.
    '''
    restro_id = order["restaurant_id"]
    order_id = order["order_id"]
    countdown = order["countdown"]

    for _ in range(countdown):
        time.sleep(1)
        # Decrement countdown for this order in the shared dictionary
        orders_by_restaurant[restro_id][order_id]["countdown"] -= 1
        
        # Remove the order if countdown reaches zero
        if orders_by_restaurant[restro_id][order_id]["countdown"] <= 0:
            orders_by_restaurant[restro_id].pop(order_id)
            break

def consume_orders():
    '''
    Kafka consumer function to continuously listen for new orders
    on the 'orders' topic. For each consumed order, it adds the order
    to orders_by_restaurant and starts a countdown_worker thread
    to handle its countdown timer asynchronously.
    '''
    consumer = KafkaConsumer(
        'orders',
        bootstrap_servers=os.environ["KAFKA_BOOTSTRAP_SERVERS"],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='order-processor-group',
    )

    for msg in consumer:
        order = msg.value
        restro_id = order["restaurant_id"]
        # Initialize dict for this restaurant if not present
        orders_by_restaurant.setdefault(restro_id, {})
        
        # Add or update order in the dictionary
        orders_by_restaurant[restro_id][order["order_id"]] = order

        # Start a new daemon thread to decrement the order's countdown
        threading.Thread(target=countdown_worker, args=(order,), daemon=True).start()
