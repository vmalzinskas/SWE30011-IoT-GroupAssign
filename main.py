from Mediator import Mediator
from Controller import Controller
from DatabaseManager import DatabaseHandler
import paho.mqtt.client as mqtt

# Callback function to handle incoming messages
def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode()} on topic {message.topic}")

if __name__ == "__main__":

    database_manager = DatabaseHandler(host="localhost", user="user1", password="password1", database="Temp")

    controllerVincent = Controller(database_manager)
    controllerAndrew = Controller(database_manager)
    controllerCharles = Controller(database_manager)


    # Create a client instance
    client = mqtt.Client()

    # Assign the on_message callback function
    client.on_message = on_message

    # Connect to the MQTT broker
    broker_address = "your_broker_address"
    broker_port = 1883
    client.connect(broker_address, broker_port)

    # Subscribe to multiple topics
    topics = [("topic1", 0), ("topic2", 0), ("topic3", 0)]
    client.subscribe(topics)

    # Start the loop to listen for messages
    client.loop_forever()

