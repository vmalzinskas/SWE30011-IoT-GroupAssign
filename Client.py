import requests
import json
from msg import message
class ServerAPI:
    def __init__(self, url, mediator):
        self.url = url
        self.mediator = mediator
        self.target_temp = None
        self.current_temp = None
    def send_to_mediator(self, msg):
        self.mediator.receive_message(message('controller', channel='set_temp', data=self.target_temp))

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
                self.current_temp = msg.get_data()
                self.run()
        elif channel == 'device_temp':
                self.default_device_temp = msg.get_data()
                self.run()
        else:
                pass


    def run(self):
        data = self.get_data()
        if data is not None and isinstance(data.get('target_temp'), float):
            # current_temp = float(input("Enter the current temperature: "))
            self.target_temp = data['target_temp']
            self.send_to_mediator(message('Controller', 'set_temp', self.target_temp))
            if self.target_temp is not None:
                self.set_data(self.current_temp, self.target_temp)
            else:
                self.set_data(self.current_temp, 'None')
        else:
            self.set_data(self.current_temp, "xxx") # this will set nothing in the target temp as it is expecting a number, either int or float or string number


    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.decoder.JSONDecodeError:
                print('Empty or invalid JSON response received')
                return None
        else:
            print('Error:', response.status_code)
            return None

    def set_data(self, current_temp, new_target_temp):
        data = {'current_temp': current_temp, 'new_target_temp': new_target_temp}
        response = requests.post(self.url, data=data)
        if response.status_code == 200:
            print('Data successfully sent to server')
            updated_data = self.get_data()  # Retrieve updated data from the server
            if updated_data:
                print('Updated Data:', updated_data)
        else:
            print('Error:', response.status_code)



if __name__ == "__main__":
    url = 'http://localhost:8000/api/endpoint'
    server_api = ServerAPI(url, mediator="m")

    data = server_api.get_data()
    if data is not None:
        current_temp = float(input("Enter the current temperature: "))
        new_target_temp = data['target_temp']
        server_api.set_data(current_temp, new_target_temp)
