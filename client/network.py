import socket
import json
import queue

from enum import Enum
from dataclasses import dataclass

from thread import threaded

BUFFER_SIZE = 128
ENCODING = "utf-8"


# possible actions to communicate with the server
class Action(str, Enum):
    START_GAME = "sg"
    REQUEST_GAME = "rg"
    READY = "r"
    SEND_MOVE = "sm"


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

        self.opponent_moves = queue.Queue()
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
    # side assigned by the server will be set to self.side
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
                self.side = response.data["side"]
                self.turn = True if self.side == "white" else False

                opponent_found = True

    # listen for an incoming move from the server
    # puts moves in the oppent_moves queue
    @threaded
    def get_opponent_moves(self):
        while True:
            response = self.get_message()
            if response.action != Action.SEND_MOVE:
                continue
            
            self.opponent_moves.put(response.data)
            self.turn = True
    
    # send a move message
    @threaded
    def send_move(self, to: int, piece_pos: int, promo_choice=None):
        msg = Message(Action.SEND_MOVE, {"to": to,
                                         "from":piece_pos,
                                         "promo_choice": promo_choice
                                         })

        self.turn = False
        self.send_message(msg)