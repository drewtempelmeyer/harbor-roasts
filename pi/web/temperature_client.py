import requests

"""Client to retrieve the current temperature reading"""
class TemperatureClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get(self):
        """Retrieve the reading from the temperature server"""
        location = "http://{0}:{1}/".format(self.host, self.port)
        response = requests.get(location)
        return r.json()

