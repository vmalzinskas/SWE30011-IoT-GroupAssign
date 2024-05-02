class TempControl:
    def __init__(self):
        # self.mediator = mediator
        self.data = None
        self.controlString = []

    def receive_data(self, data):
        # print("tempcontrol ", data)
        self.data = data
        self.process_data()

    def process_data(self):
        # print("tempcontrol process data")
        if self.data[3] < 0: 
            self.controlString.append('h') #turn on fan
            self.controlString.append('0') #open valve
        if self.data[3] > 0:
            self.controlString.append('s') #turn off fan
            self.controlString.append('1') #close valve

    def get_control_string(self):
        lcontrolString = self.controlString.copy()
        self.controlString.clear()
        return lcontrolString

