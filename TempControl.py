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
        # data[3] is the degree C from the tageted temp. -20 mean target temp is 20 degrees below current
        # self.data[4] is the degree C outside from the tageted temp. -20 mean target temp is 20 degrees below current
        temp_adustment = self.data[3] + self.data[4]

        # print(f"temp outside: {self.data[4]}\ntemp inside: {self.data[3]}")
        # print(f"temp adjustment {temp_adustment}")
        if self.data[3] < 0:
            # print("cooling needed")
            if self.data[4] < -10:
                # print("high")
                self.controlString.append('h') #turn on fan high
                self.controlString.append('0') #open valve
            if -10 <= self.data[4] < -5:
                # print("med")
                self.controlString.append('m') #turn on fan medium
                self.controlString.append('0') #open valve
            if -5 <= self.data[4] < 0:
                # print("low")
                self.controlString.append('l') #turn on fan low
                self.controlString.append('0') #open valve
        if self.data[3] > 0:
            self.controlString.append('s') #turn off fan
            self.controlString.append('1') #close valve

    def get_control_string(self):
        lcontrolString = self.controlString.copy()
        self.controlString.clear()
        return lcontrolString

