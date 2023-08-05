import json
import requests
from datetime import datetime, timedelta
import os
import websocket
#from .client_api import Gardena_Client_api
from threading import Thread

AUTHENTICATION_HOST = 'https://api.authentication.husqvarnagroup.dev/v1/oauth2/token'
SMART_HOST_LOCATION = 'https://api.smart.gardena.dev/v1/locations'
SMART_HOST_WEBSOCKET = 'https://api.smart.gardena.dev/v1/websocket'
SMART_HOST_COMMAND = 'https://api.smart.gardena.dev/v1/command/'


class Client:
    def __init__(self, smart_system=None):
        self.smart_system = smart_system
        self.live = False

    def on_message(self, message):
        self.msg = json.loads(message)
        self.document = ""
        if self.msg["type"] == "VALVE":
            self.document = self.get_valve_name() + self.get_valve_activity()
            print("Id ", self.get_valve_id())
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

        #def run(*args):
        #    while self.live:
        #        time.sleep(1)
        #Thread(target=run).start()

    def get_valve_id(self):
        return self.msg["id"]
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


class Gardena(object):
    """Class to take care of cummunication with Gardena Smart system"""
    def __init__(self, email_address=None, password=None, api_key=None):
        if email_address ==None or password==None:
            raise ValueError('Please provide, email, password')
        self.debug=True
        self.s = requests.session()
        self.email_address = email_address
        self.password = password
        self.api_key = api_key
        self.update()

    def update(self):
        self.get_authtokens()
        self.get_locations()
        self.get_websocket_url()

    def get_authtokens(self):
        """Get authentication token from servers"""
        payload = {'grant_type': 'password', 'username': self.email_address, 'password': self.password,
               'client_id': self.api_key}

        print("Logging into authentication system...")
        r = requests.post(AUTHENTICATION_HOST, data=payload)
        assert r.status_code == 200, r
        auth_token = r.json()["access_token"]
        self.authToken = r.json()["access_token"]
        if r.status_code == 200:
            self.isLoggedIn = True
        else:
            self.isLoggedIn = False

    def get_locations(self):
        print("Getting locationid...")
        headers = {
            "Content-Type": "application/vnd.api+json",
            "x-api-key": self.api_key,
            "Authorization-Provider": "husqvarna",
            "Authorization": "Bearer " + self.authToken
        }

        r = requests.get(SMART_HOST_LOCATION, headers=headers)
        assert r.status_code == 200, r
        assert len(r.json()["data"]) > 0, 'location missing - user has not setup system'

        self.locationId = r.json()["data"][0]["id"]

    def set_watering(self, deviceid=None, timer=None):
        if timer == None:
            timer = 1800
        if deviceid == None:
            return "No deviceid"
        self.deviceid = deviceid
        deviceidURL = SMART_HOST_COMMAND + self.deviceid
        print("Watering started with (%s)" % timer)
        headers = {
            "Content-Type": "application/vnd.api+json",
            "x-api-key": self.api_key,
            "Authorization-Provider": "husqvarna",
            "Authorization": "Bearer " + self.authToken
        }

        data = {
            "data": {
                "id": "request-1",
                "type": "VALVE_CONTROL",
                "attributes": {
                    "command": "START_SECONDS_TO_OVERRIDE",
                    "seconds": timer
                }
            }
        }
        print("Calling Gardena with URL: %s" % deviceidURL)
        r = requests.put(deviceidURL, headers=headers, json=data)
        assert r.status_code == 202, r
        print(r.status_code)

        return r.status_code
        #assert len(r.json()["data"]) > 0, 'smart control command'

        #self.locationId = r.json()["data"][0]["id"]

    def get_websocket_url(self):
        print("Getting websocketurl...")
        payload = {
            "data": {
                "type": "WEBSOCKET",
                "attributes": {
                    "locationId": self.locationId
                },
                "id": "does-not-matter"
            }
        }
        headers = {
            "Content-Type": "application/vnd.api+json",
            "x-api-key": self.api_key,
            "Authorization-Provider": "husqvarna",
            "Authorization": "Bearer " + self.authToken
        }
        print("Logged in (%s), getting WebSocket ID..." % self.authToken)
        r = requests.post(SMART_HOST_WEBSOCKET, json=payload, headers=headers)

        assert r.status_code == 201, r
        print("WebSocket ID obtained, connecting...")
        response = r.json()
        self.websocket_url = response["data"]["attributes"]["url"]
        print("WebSocket URL obtained: %s" % self.websocket_url)

    def start_ws(self, websocket_url):
        self.ws_url = websocket_url
        self.client = Client(self)

        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self.client.on_message,
            on_error=self.client.on_error,
            on_close=self.client.on_close,
            on_open=self.client.on_open)

        wst = Thread(
            target=self.ws.run_forever, kwargs={"ping_interval": 60, "ping_timeout": 5}
        )
        wst.daemon = True
        wst.start()
        wst.join()

    def debug_print(self, string):
        if self.debug:
            print(string)

    def isLoggedIn(self):
        return self.isLoggedIn
