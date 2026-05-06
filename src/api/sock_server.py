# server
import socket, os, time, threading, json
from api.api_call import api_call


class SockAdapter:
    def __init__(self, PATH="/tmp/chat.sock"):
        self.path = PATH
        try:
            os.unlink(self.path)
        except FileNotFoundError:
            pass
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.bind(self.path)
        self.s.listen(1)
        self.conn, _ = self.s.accept()
        threading.Thread(target=self.recv_loop, daemon=True).start()

    def send(self, msg):
        self.conn.sendall(msg.encode())

    def recv_loop(self):
        while 1:
            data = self.conn.recv(1024)
            if not data:
                break
            print("DATA RECIEVED:", data.decode())
            data_list = data.decode().split("\n")

            for data in data_list:
                print("DATA:", data)
                if not data:
                    continue
                data = json.loads(data)
                """ data format
                data = {
                    "action": "api_call",
                    "content": str,
                    "opts":{tbd},
                }
                """
                if data.get("action") == "api_call":
                    # call
                    if data.get("content"):
                        api_call(self, prompt=data.get("content"))
                else:
                    pass
                print(data)


s = SockAdapter()
while 1:
    if not s.conn:
        continue
    time.sleep(0.1)
    s.send("test data")
