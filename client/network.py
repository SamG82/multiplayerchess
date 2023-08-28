import socket
import json
import queue

from enum import Enum
from dataclasses import dataclass

from thread import threaded

BUFFER_SIZE = 1024
ENCODING = "utf-8"


# possible actions to communicate with the server
class Action(str, Enum):
    START_GAME = "sg"
    REQUEST_GAME = "rg"
    READY = "r"
    SEND_MOVE = "sm"
    UPDATE_BOARD = "ub"
    CONCLUDE = "c"


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

        self.messages = queue.Queue()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.color = None

    # connect the socket
    def connect(self):
        self.socket.connect((self.server_address, self.server_port))
    
    # read one message from the socket
    def get_message(self):
        resp_bytes = self.socket.recv(BUFFER_SIZE)
        return Message.from_json_bytes(resp_bytes)
    
    # send a message's json bytes to the socket
    def send_message(self, msg: Message):
        self.socket.send(msg.to_json_bytes())

    # sends a start game message to the server
    # side assigned by the server will be set to self.color
    @threaded
    def request_game(self):
        msg = Message(Action.REQUEST_GAME, {})
        self.send_message(msg)
        
        opponent_found = False

        while not opponent_found:
            response = self.get_message()

            # send a ready message if the server is checking 
            if response.action == Action.READY:
                self.send_message(Message(Action.READY, {}))

            # opponent was found and game is starting
            elif response.action == Action.START_GAME:
                self.color = response.data["color"]
                self.messages.put(response)
                opponent_found = True

    # listen for incoming communication, puts them in self.messages queue
    @threaded
    def listen(self):
        while True:
            msg = Message.from_json_bytes(self.socket.recv(BUFFER_SIZE))
            self.messages.put(msg)

    # send a move message
    @threaded
    def send_move(self, from_square: str, to_square: str, promotion_choice=None):
        data = {"move": f"{from_square}{to_square}"}
        if promotion_choice:
            data["move"] += promotion_choice
        
        self.send_message(Message(Action.SEND_MOVE, data))
