class message:
    def __init__(self, receiver, data, channel='default'):
        self.receiver = receiver
        self.data = data
        self.channel = channel

    def get_receiver(self):
        return self.receiver

    def get_channel(self):
        return self.channel

    def get_data(self):
        return self.data

