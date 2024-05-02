class Mediator:
    def __init__(self):
        self.comms_list = {}
        self.message_list = []
    def add_to_comms(self, id, receiver):
        self.comms_list[id] = receiver

    def receive_message(self, msg):
        # print("mediator ", msg.get_data())
        self.message_list.append(msg)
    def send_messages(self):
        for msg in self.message_list:
            self.comms_list[msg.receiver].receive_message(msg)
        self.message_list.clear()

