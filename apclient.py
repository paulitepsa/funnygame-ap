import multiprocessing
import weakref
import asyncio
import websockets
import ssl
import json
import uuid
import signal
from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection
import pygame


class APClient:
    def __init__(self):
        self.game_name: str = "Funnygame"
        self.protocol: str = "wss://"
        self.server_address: str = "archipelago.gg"
        self.password: str
        self.username: str
        self.uuid_str: str
        self.received_items: dict = None
        self.connected: bool = False
        self.player_id: int
        self.game_won: False
        self.socket: websockets
        self.AP_EVENT = pygame.event.custom_type()
        self.AP_LOCATION_CHECK_EVENT = pygame.event.custom_type()

    async def run_archipelago(self, future, c_info):
        try:
            is_ssl = await self.check_ssl(c_info[0])
            if is_ssl is True:
                self.protocol = "wss://"
            else:
                self.protocol = "ws://"
            await self.handle_connection_info(c_info)

            try:
                await self.handle_connect()
            except websockets.ConnectionClosedError as err:
                print("ERROR", err)
                self.protocol = "ws://"
                await self.handle_connect()

        except ConnectionError:
            print(f"Could not connect {ConnectionError}")

    def get_received_items(self):
        if self.connected:
            return self.received_items

    def get_player_info(self):
        return {"name": self.username, "id": self.player_id}

    async def check_ssl(self, baseurl):
        HTTPS_URL = f"https://{baseurl}"
        try:
            HTTPS_URL = urlparse(HTTPS_URL)
            connection = HTTPSConnection(HTTPS_URL.netloc, timeout=2)
            connection.request("HEAD", HTTPS_URL.path)
            if connection.getresponse():
                print("The server has SSL")
                return True
            else:
                print("The server doesn't have SSL")
                return False

        except:
            return False

    async def handle_connect(self):

        try:
            async with websockets.connect(self.server_address) as websocket:
                c_id = uuid.uuid4()
                self.uuid_str = str(c_id)
                self.socket = websocket
                res = await websocket.recv()
                self.connected = False

                while not self.connected:
                    if res:
                        print("RES:", res)
                        connect_data = json.dumps(
                            [
                                {
                                    "cmd": "Connect",
                                    "password": self.password,
                                    "game": self.game_name,
                                    "name": self.username,
                                    "uuid": self.uuid_str,
                                    "version": {
                                        "major": 0,
                                        "minor": 6,
                                        "build": 1,
                                        "class": "Version",
                                    },
                                    "items_handling": 0b001,
                                    "tags": [],
                                    "slot_data": True,
                                }
                            ]
                        )
                        print(connect_data)
                        await websocket.send(connect_data)
                        connect_response = await websocket.recv()
                        if connect_response:
                            print(connect_response)
                            res_dict = json.loads(connect_response)
                            for res in res_dict:

                                if res["cmd"] == "Connected":
                                    self.player_id = res["slot"]
                                    print("SLOT", self.player_id)
                                if res["cmd"] == "ReceivedItems":

                                    self.handle_message(json.dumps([res]))
                                else:
                                    print(res)
                            self.connected = True

                async for message in websocket:
                    try:
                        self.handle_message(message)
                    except ConnectionError:
                        print("failed to handle messages in websocket")
                        self.connected = False

        except ssl.SSLError:
            print("connection closed, retrying")

    async def handle_connection_info(self, c_info):
        self.server_address = f"{self.protocol}{c_info[0]}"
        self.username = c_info[1]
        self.password = c_info[2]

    async def send_check(self, msg, socket):
        if not socket:
            socket = self.socket
        print("MSG", msg)
        await socket.send(msg)

    def handle_message(self, message):

        msg = json.loads(message)

        match msg[0]["cmd"]:
            case "Connected":
                print(msg[0])
                pygame.fastevent.post(pygame.event.Event(self.AP_EVENT, message=msg[0]))
            case "PrintJSON":
                print(msg[0])
                pygame.fastevent.post(pygame.event.Event(self.AP_EVENT, message=msg[0]))
            case "ReceivedItems":
                print("RECEIVED ITEMS:", msg[0])
                r_items = msg[0]
                self.received_items = r_items
                pygame.fastevent.post(
                    pygame.event.Event(self.AP_EVENT, message=r_items)
                )
            case "LocationChecks":
                print("SENDING ITEM", message)
                pygame.fastevent.post(pygame.event.Event(self.AP_EVENT, message=msg[0]))
                asyncio.run(self.send_check(message, self.socket))
            case "W":
                print("SENDING WIN")
                win_location = {"locations": [3551]}
                asyncio.run(self.send_check(win_location, self.socket))
            case _:
                print("Not relevant message", msg)


def main(future, c_info):
    ap = APClient()
    asyncio.run(ap.run_archipelago(future, c_info))
