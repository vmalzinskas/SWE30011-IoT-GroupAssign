from TempControl import TempControl
from TempStats import TempStats
from msg import message
from WeatherAPI import WeatherApiClient

class Controller:
    def __init__(self, mediator, arduino, databasemanager, target_temp):
        self.mediator = mediator
        self.temp_control = TempControl()
        self.temp_stats = TempStats(target_temp)
        self.data = None
        self.stats = None
        self.controlString = ['', '']
        self.local_temp_api = WeatherApiClient(latitude=-37.814, longitude=144.9633, timezone="GMT")
        # self.temp_control.set_receiver(arduino)
        # self.temp_stats.set_receiver(databasemanager)

    # def set_receiver(self, receiver):
    #     self.mediator.add_to_comms(self, receiver)
    def send_to_mediator(self, msg):
        self.mediator.receive_message(msg)

    def receive_message(self, msg):
        channel = msg.get_channel()
        if channel == 'default':
            self.data = msg.get_data()
            self.process_data()
        elif channel == 'set_temp':
            self.set_temp(msg.data)
        elif channel == 'user':
            self.process_user(msg.data)
        else:
            # Handle other cases if needed
            pass

    def process_user(self, data):
        time_str, temp_str, humid_str, user = data.split(',')
        # print(f"controller {user}")
        if (user == '03d7ddb6'):
            self.set_temp(23)
            self.send_to_mediator(message('webserver', 23, 'user_target_temp'))
            print('accepted user')

    def set_temp(self, temp):
        # update stats and control with new ideal temp
        self.temp_stats.set_temp(temp)

    def get_temp(self):
        return self.temp_stats.get_temp()
    # def export_data(self):
    #     self.set_receiver()
    #     self.mediator.pass_data(self.data)

    def process_data(self):
        nextHourTemp = self.local_temp_api.get_next_hour_temperature()
        self.temp_stats.set_next_hour_temp(nextHourTemp);
        # print(f'Controller, nextHourTemp {nextHourTemp}')
        self.temp_stats.receive_data(self.data)
        self.stats = self.temp_stats.export_stats()
        if self.stats is not None:
            self.send_to_mediator(message('databaseManager', self.stats))
            self.control = self.temp_control.receive_data(self.stats)
            self.controlString = self.temp_control.get_control_string()
        self.send_to_mediator(message('arduino', self.controlString))
        # print(f"temp sent to webserver {self.get_temp()}")
        self.send_to_mediator(message('webserver', self.get_temp()))
