from flask import Flask, request
from flask_socketio import SocketIO, emit
from order_processor import orders_by_restaurant, consume_orders
import threading
import os

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    '''
    Root endpoint returning a simple message to indicate
    that the Order Tracker WebSocket API is running.
    '''
    return "Order Tracker WebSocket API"

@socketio.on("subscribe")
def handle_subscribe(data):
    '''
    Socket.IO event handler for "subscribe" event.
    Receives a restaurant_id from the client and starts
    a background task that sends real-time order updates
    for that restaurant every second.
    
    Parameters:
    - data: dict containing "restaurant_id" key
    '''
    restro_id = data.get("restaurant_id")
    sid = request.sid

    def send_updates():
        '''
        Background task that runs in an infinite loop,
        emitting the current list of orders for the subscribed
        restaurant to the client every 1 second.
        Prints debug info if no orders found.
        '''
        while True:
            if restro_id in orders_by_restaurant:
                orders = list(orders_by_restaurant[restro_id].values())
                print(f"Sending orders to {restro_id}: {orders}")
                socketio.emit("order_update", {"orders": orders}, to=sid)
            else:
                print(f"No orders found for {restro_id}")

            socketio.sleep(1)

    # Start the background task to send order updates
    socketio.start_background_task(send_updates)


if __name__ == "__main__":
    '''
    Starts the Kafka consumer in a separate daemon thread
    to populate orders_by_restaurant continuously.
    Then runs the Flask-SocketIO server on dedicated port
    '''
    threading.Thread(target=consume_orders, daemon=True).start()
    socketio.run(app, debug=True, port= int(os.environ['APP_PORT']))