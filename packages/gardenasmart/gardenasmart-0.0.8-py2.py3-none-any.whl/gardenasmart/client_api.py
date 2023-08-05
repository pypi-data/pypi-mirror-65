import json
from datetime import datetime, timedelta
import os
import websocket

class Gardena_Client_api(object):
    """Class to take care of cummunication with Gardena Smart system"""
    def __init__(self, websocket_url=None):
        if websocket_url ==None:
            raise ValueError('No websocket url')
        self.debug=True

        self.websocket_url = websocket_url
        print("Websocket connection...")
        print("Websocket URL: " + websocket_url)
        client = Client()
        while True:
            ws = websocket.WebSocketApp(
                self.websocket_url,
                on_message=client.on_message,
                on_error=client.on_error,
                on_close=client.on_close)
            ws.on_open = client.on_open
            ws.run_forever(ping_interval=150, ping_timeout=1)

    def debug_print(self, string):
        if self.debug:
            print(string)

class Client:
    def on_message(self, message):
        self.msg = json.loads(message)
        self.document = ""
        if self.msg["type"] == "VALVE":
            self.document = self.get_valve_name() + self.get_valve_activity()
            print("Name ", self.get_valve_name())
            print("Activity: ", self.get_valve_activity())
            print("Timestamp Activity: ", self.get_valve_activity_timestamp() )
            print("State: ", self.get_valve_state())
            print("Timestamp State: ", self.get_valve_state_timestamp() )
            print("Lasterror: ", self.get_valve_lasterror())
            print("Timestamp Lasterror: ", self.get_valve_lasterror_timestamp() )
            print("Document: ", self.document)
        elif self.msg["type"] == "COMMON":
            print("Name: ", self.get_common_name())
            print("batteryState: ", self.get_common_batteryState())
            print("rfLinkLevel: ", self.get_common_rfLinkLevel())
            print("serial: ", self.get_common_serial())
            print("modelType: ", self.get_common_modelType())
            print("rfLinkState: ", self.get_common_rfLinkState())
        sys.stdout.flush()

    def on_error(self, error):
        print("error 1", error)
        ws.close()

    def on_close(self):
        self.live = False
        print("### closed ###")

    def on_open(self):
        self.live = True

        def run(*args):
            while self.live:
                time.sleep(1)
        Thread(target=run).start()

    def get_valve_name(self):
        return self.msg["attributes"]["name"]["value"]
    def get_valve_activity(self):
        return self.msg["attributes"]["activity"]["value"]
    def get_valve_activity_timestamp(self):
        return self.msg["attributes"]["activity"]["timestamp"]
    def get_valve_state(self):
        return self.msg["attributes"]["state"]["value"]
    def get_valve_state_timestamp(self):
        return self.msg["attributes"]["state"]["timestamp"]
    def get_valve_lasterror(self):
        return self.msg["attributes"]["lastErrorCode"]["value"]
    def get_valve_lasterror_timestamp(self):
        return self.msg["attributes"]["lastErrorCode"]["timestamp"]
    def get_common_name(self):
        return self.msg["attributes"]["name"]["value"]
    def get_common_batteryState(self):
        return self.msg["attributes"]["batteryState"]["value"]
    def get_common_rfLinkLevel(self):
        return self.msg["attributes"]["rfLinkLevel"]["value"]
    def get_common_serial(self):
        return self.msg["attributes"]["serial"]["value"]
    def get_common_modelType(self):
        return self.msg["attributes"]["modelType"]["value"]
    def get_common_rfLinkState(self):
        return self.msg["attributes"]["rfLinkState"]["value"]
