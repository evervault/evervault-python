class Cage(object):
    def __init__(self, name, uuid, client):
        self.name = name
        self.uuid = uuid
        self.client = client

    def run(self, data):
        return self.client.run(self.name, data)
