# Kafka Real-Time Order Tracker Demo

## Overview

This demo app demonstrates a real-time order tracking system using Apache Kafka and Flask-SocketIO.  
Orders from multiple restaurants are produced, consumed, processed with countdown timers, and pushed in real-time to clients subscribed via WebSocket.

## Components

- **Producer (`producer.py`)**: Simulates order creation and sends order events to Kafka topic `orders`.
- **Consumer/Processor (`order_processor.py`)**: Consumes `orders` from Kafka, groups them by restaurant, and maintains countdown timers for each order.
- **WebSocket API (`app.py`)**: Flask app with SocketIO that allows clients to subscribe to restaurant-specific orders and receive real-time countdown updates.
- **Frontend (`index.html`)**: Simple HTML page to display real-time orders for a specific restaurant.

## Setup

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Python 3.8+
   - Kafka and Zookeeper running (via Docker Compose or standalone)

2. **Start Kafka and Zookeeper:**

```bash
docker-compose up -d
```

3. **Create a `.env` file** (sample):

```env
ZOOKEEPER_CLIENT_PORT=2181
ZOOKEEPER_TICK_TIME=2000
KAFKA_BROKER_ID=1
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1
KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT
KAFKA_AUTO_CREATE_TOPICS_ENABLE=true
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
APP_PORT=5000
```

4. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

5. **Run the Producer:**

```bash
python producer.py
```

6. **Run the Consumer/Processor:**

```bash
python order_processor.py
```

7. **Run the WebSocket API Server:**

```bash
python app.py
```

8. **Open `index.html` in your browser** to view real-time orders for a restaurant.

## Workflow

- Producer sends orders to Kafka topic `orders`.
- Consumer listens to `orders` topic, stores orders grouped by restaurant, and runs a countdown timer that decrements every second.
- Flask-SocketIO app allows clients to subscribe to a restaurant’s orders.
- Clients receive real-time updates every second with current countdown values for their subscribed restaurant orders.

## Notes

- Kafka consumer uses a consumer group to ensure load balancing and fault tolerance.
- Countdown is implemented via threads for demo purposes.
- This demo is minimal and intended for learning purposes.

---

Feel free to customize and extend this demo for your use case!

---