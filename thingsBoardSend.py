
import paho.mqtt.client as paho
from paho.mqtt import client as mqtt_client
from msg import message

class ThingsBoardCtrl:
    def __init__(self, mediator):
        self.mediator = mediator
        self.data = None
        self.client1= paho.Client(mqtt_client.CallbackAPIVersion.VERSION2 , client_id="2x0Wmp5bMNtXOAfGIbum")
        self.client1.on_publish = on_publish
        self.client1.username_pw_set('2x0Wmp5bMNtXOAfGIbum')               
        self.client1.connect("thingsboard.cloud",1883,keepalive=60)
        self.client1.on_connect = on_connect

    def send_to_mediator(self, msg):
        self.mediator.receive_message(msg)

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.data = msg.get_data()
            self.process_data()
        #elif channel == '':
            # do thing
        else:
            # Handle other cases if needed
            pass

        #client_id should be the token
    def process_data(self):
        data = self.data.split(',')

        payload = f'''{{
                     "Uptime":"{data[0]}",
                     "temperature": {data[1]},
                     "humidity": {data[2]},
                     "User": "{data[3]}",
                     "room": "{data[4]}"
                     }}'''
        # payload=f'{{"data":{data}}}'
        # payload = '{Temperature:0, Bob:5}'
        ret = self.client1.publish("v1/devices/me/telemetry",payload)
        print("Device telemetry updated")
        print(payload);

def on_publish(client,userdata,result, reasoncode, properties):
    print("data published to thingsboard \n")

def on_connect(client, userdata, flags, rc):
    flag_connected = 1
    print (flag_connected )
