import random
import threading
import time

from .parser import Parser


class Server:

    def __init__(self):
        self.handlers = {}
        self.clients = {}
        self.controllers = {}
        self.pilots = {}
        self.folme = {}
        self.update_stream = threading.currentThread()

    def call(self, name, *args):
        """
        Call a registed event by the name with arguments
        :param name: Event Name
        :param args: Argument to pass
        """
        if name in self.handlers:
            for h in self.handlers[name]:
                h(*args)

    def event(self, name):
        """
        Registering events by name
        :param name: Name of the event
        :return: event handler
        """

        def registerhandler(handler):
            if name in self.handlers:
                self.handlers[name].append(handler)
            else:
                self.handlers[name] = [handler]
            return handler

        return registerhandler

    def update_data(self, data=None):
        """
        Updating function that calls event triggers
        :param data: New data to compare
        """
        if not data:
            parser = Parser()
            data = parser.get_clients_object()
        first_run = True if len(self.clients) == 0 else False
        for client in data['atc']:
            if client.vid in self.controllers:  # If client was connected at previous update
                if self.controllers[client.vid].atis_time != client.atis_time:
                    self.call("atis_update", client)
            else:  # Client connected since last update
                self.call("connect", client, first_run)
            self.controllers[client.vid] = client
            self.clients[client.vid] = client
        for client in data['pilot']:
            if client.vid in self.pilots:  # If client was connected at previous update
                if self.pilots[client.vid].ground != client.ground:
                    if client.ground:
                        self.call("land", client)
                    else:
                        self.call("takeoff", client)
                if self.pilots[client.vid].latitude == client.latitude \
                        and self.pilots[client.vid].longitude == client.longitude \
                        and self.pilots[client.vid].altitude == client.altitude:
                    self.call("static", client)
                else:
                    self.call("moving", client)
            else:  # Client connected since last update
                self.call("connect", client, first_run)
            self.pilots[client.vid] = client
            self.clients[client.vid] = client
        for client in data['folme']:
            if client.vid in self.folme:  # If client was connected at previous update
                pass
            else:  # Client connected since last update
                self.call("connect", client, first_run)
            self.folme[client.vid] = client
            self.clients[client.vid] = client
        disconnects = []
        for vid in self.clients:
            still_connected = False
            for client in data['atc']:
                if client.vid == vid:
                    still_connected = True
                    break
            for client in data['pilot']:
                if client.vid == vid:
                    still_connected = True
                    break
            for client in data['folme']:
                if client.vid == vid:
                    still_connected = True
                    break
            if not still_connected:
                self.call("disconnect", self.clients[vid])
        for vid in disconnects:
            self.clients.pop(vid)

        self.call('update', self.clients)

    def stop_update_stream(self):
        """
        Request updates stop, because it's running in a separate thread
        """
        self.update_stream.do_run = False

    def run_update_stream(self, delay=None):
        """
        Start updates runner
        :param delay: Delay, in minutes,
        """
        while getattr(self.update_stream, "do_run", True):
            self.update_data()
            if delay:
                time.sleep(delay * 60)
            else:
                time.sleep(random.randint(1, 3) * 60)
