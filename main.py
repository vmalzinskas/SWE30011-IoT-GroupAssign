from Mediator import Mediator
from Controller import Controller
from ArduinoConn import ArduinoConnection
from DatabaseManager import DatabaseHandler
from Client import ServerAPI
from thingsBoardSend import ThingsBoardCtrl


if __name__ == "__main__":
    target_temp = 0
    url = 'http://0.0.0.0:8000/api/endpoint'

    # Create an instance of the Mediator class
    mediator = Mediator()

    arduino = ArduinoConnection(mediator)
    database_manager = DatabaseHandler(host="localhost", user="user1", password="password1", database="Temp")
    controller = Controller(mediator, arduino, database_manager, target_temp=target_temp)
    Client = ServerAPI(mediator=mediator, url=url)
    thingsB = ThingsBoardCtrl(mediator)

    mediator.add_to_comms('databaseManager', database_manager)
    mediator.add_to_comms('arduino', arduino)
    mediator.add_to_comms('controller', controller)
    mediator.add_to_comms('webserver', Client)
    mediator.add_to_comms('thingsboard', thingsB)

    # Create the root window for GUI (if needed)
    # root = Tk()
    # Create an instance of the VariableDisplayGUI class (if needed)
    # variable_display = VariableDisplayGUI(root, mediator, target_temp)

    # Main loop of your program
    while True:
        arduino.receive_data()
        mediator.send_messages()
