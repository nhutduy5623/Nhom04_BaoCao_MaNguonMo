import socket
import pickle
import requests
HOST = "0.tcp.ap.ngrok.io"
PORT = 0

HOST = "localhost"
PORT = 65432
class Network():
    def __init__(self,host,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(5)
        print(host)
        print(port)

        self.host = HOST
        self.port = PORT
        self.id = self.connect_and_join(HOST, PORT)

    def setNAR(self, room_id, name):
        self.room_id = room_id
        self.name = name
        message = f"JOIN {room_id} AS {name}"
        self.client.send(message.encode())
        data = self.client.recv(1024).decode()
        if data.find("host") != -1:
            return True
        else:
            return False

    def connect_and_join(self,host,port):
        try:
            self.client.connect((host, port))
            return 1
        except:
            pass

    def sendData(self, data):
        try:
            self.client.send(data.encode())
            data = self.client.recv(1024).decode()
            return data
        except:
            pass

    def GetObs(self, data):
        try:
            self.client.send(data.encode())
            data = self.client.recv(1024)
            data = pickle.loads(data)
            return data
        except:
            return None
