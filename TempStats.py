from datetime import datetime
import numpy as np

class TempStats:
    def __init__(self, target_temp):
        # self.mediator = mediator
        self.data = None
        self.target_temp = target_temp

        self.timeData = []
        self.tempData = []
        self.humidData = []
        self.deltaTempSec = 0
        self.degreeCfromIdeal = 0
        self.user = None

        self.stats = None
        self.next_hour_temp = None

    def get_humidity(self):
        return self.humidData[-1]

    def set_temp(self, temp):
        self.target_temp = temp

    def get_temp(self):
        # print("returning temp to controller")
        return self.tempData[-1]

    def set_next_hour_temp(self, temp):
        self.next_hour_temp = temp


    def receive_data(self, data):
        # print("tempStats ", data)
        self.data = data
        self.process_data()
        self.calcStats()

    def export_stats(self):
        return self.stats
    def process_data(self):
        try:
            # Split the string at the comma to separate time and temperature
            time_str, temp_str, humid_str, user = self.data.split(',')

            # Convert temperature string to float
            temperature = float(temp_str)
            humidity = float(humid_str)

            # Parse time string to datetime object
            time_format = "%H:%M:%S"  # Adjust this format based on your time format
            time_obj = datetime.strptime(time_str, time_format)

            # Store time and temperature data in lists or process further as needed
            self.timeData.append(time_obj)  # Store time data
            self.tempData.append(temperature)  # Store temperature data
            self.humidData.append(humidity)
            self.user = user
        except ValueError:
            print("Invalid temperature value:", temp_str)

    def calcStats(self):
        if len(self.timeData) > 1:
            current_humidity = self.humidData[-1]
            current_time = self.timeData[-1]
            previous_time = self.timeData[-2]
            current_temp = self.tempData[-1]
            previous_temp = self.tempData[-2]
            deltaTime = (current_time - previous_time).total_seconds()
            deltaTemp = current_temp - previous_temp
            self.deltaTime = deltaTime
            self.deltaTempSec = np.round(deltaTemp / deltaTime, 2)
            self.degreeCfromIdeal = np.round(self.target_temp - current_temp, 2)
            degreeCfromIdealNextHour = np.round(self.target_temp - self.next_hour_temp, 2)
            self.stats = [current_temp, current_humidity, self.deltaTempSec, self.degreeCfromIdeal, degreeCfromIdealNextHour]
