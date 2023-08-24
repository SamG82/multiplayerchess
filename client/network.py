import socket
import json
from enum import Enum
from dataclasses import dataclass

BUFFER_SIZE = 128
ENCODING = "utf-8"

# possible actions to communicate with the server
class Action(str, Enum):
    START_GAME = "sg"
    REQUEST_GAME = "rg"
    READY = "r"

# represents a message sent between client and server
@dataclass
class Message:
    action: Action
    data: dict
    
    # returns a message object created from raw json bytes
    @staticmethod
    def from_json_bytes(json_bytes: bytes):
        msg_json = json.loads(json_bytes)
        return Message(msg_json["action"], msg_json["data"])
    
    # returns the message represented as json bytes
    def to_json_bytes(self):
        payload = {
            "action": self.action,
            "data": self.data
        }

        json_str = json.dumps(payload)
        return bytes(json_str, ENCODING)

class Client:

    def __init__(self, server_address: str, server_port: str):
        self.server_address = server_address
        self.server_port = server_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the socket
    def connect(self):
        self.socket.connect((self.server_address, self.server_port))
    
    # read one message from the socket
    def get_message(self):
        return Message.from_json_bytes(self.socket.recv(BUFFER_SIZE))
    
    # send a message's json bytes to the socket
    def send_message(self, msg: Message):
        self.socket.send(msg.to_json_bytes())

    # sends a start game message to the server
    # stores the assigned side from the server in result_store when done
    def request_game(self, result_store: dict):
        msg = Message(Action.REQUEST_GAME, {})
        self.socket.send(msg.to_json_bytes())
        
        side = ""
        opponent_found = False

        while not opponent_found:
            response = self.get_message()

            # send a ready message if the server is checking 
            if response.action == Action.READY:
                self.send_message(Message(Action.READY, {}))

            # opponent was found and game is starting
            elif response.action == Action.START_GAME:
                side = response.data["side"]
                opponent_found = True
        
        result_store["side"] = side