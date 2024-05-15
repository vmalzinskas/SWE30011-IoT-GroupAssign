
import paho.mqtt.client as paho
from paho.mqtt import client as mqtt_client
from msg import message

class ThingsBoardCtrl:
    def __init__(self, mediator):
        self.mediator = mediator
        self.data = None
        self.start()

    def start(self):
        self.client1 = paho.Client(client_id="2x0Wmp5bMNtXOAfGIbum", protocol=paho.MQTTv5)
        self.client1.on_publish = on_publish
        self.client1.username_pw_set('2x0Wmp5bMNtXOAfGIbum')   # Vincent's access token: '2x0Wmp5bMNtXOAfGIbum'   # Charles' access token: 'E3TRclyItqtBWnAhnxWO'  # Andrew's access token: 'kS2cHltahsgAc6Zju3xR'
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
                     "User": "{data[3]}"
                     }}'''
        # payload=f'{{"data":{data}}}'
        # payload = '{Temperature:0, Bob:5}'
        ret = self.client1.publish("v1/devices/me/telemetry",payload)
        # print("Device telemetry updated") #################### uncomment here to see telemetry data pushed
        # print(payload); #################### uncomment here to see telemetry data pushed

def on_publish(client, userdata, mid):
    pass
    # print("Data published to ThingsBoard with message id:", mid)



def on_connect(client, userdata, flags, rc):
    flag_connected = 1
    print (flag_connected )
