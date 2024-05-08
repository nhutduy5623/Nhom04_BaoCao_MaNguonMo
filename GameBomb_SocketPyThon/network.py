import socket
from DTO.playerDTO import PlayerDTO
from DTO.battlegroundDTO import BattleGroundDTO
import pickle
import SystemVariable

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SystemVariable.serverIP
        self.port = SystemVariable.port
        self.addr = (self.server, self.port)
        self.battleGround = self.connect()

    def getPlayer(self):
        return self.player
    
    def getBattleGround(self):
        return self.battleGround

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)