import serial
from msg import message
import time

class ArduinoConnection:
    def __init__(self, mediator):
        self.serial_device = None
        # Establish connection to serial device
        try:
            self.serial_device = serial.Serial('/dev/ttyS0', 9600)  # Change 'COM4' to the appropriate COM port
        except serial.SerialException:
            print("Warning: Failed to establish connection to COM4.")
        self.data = None
        self.mediator = mediator
        # self.messageList = []
        self.control_string = []

    def send_to_mediator(self):
        self.mediator.receive_message(message('controller', self.data))

    def receive_message(self, msg):
        # print('arduino ',  msg.get_data())
        self.control_string = msg.get_data()
        self.send_control_to_device()

    def receive_data(self):
        # Read data from serial device and pass it to the controller
        try:
            self.data = self.serial_device.readline().decode().strip()
            self.send_to_mediator()
        except Exception as e:
            print("Warning: Failed to read data from serial device:", e)
            time.sleep(1)

    def send_control_to_device(self):
        for command in self.control_string:
            # print('command', command.encode('utf-8')) #send in bytes
            self.serial_device.write(command.encode('utf-8'))
