import socket, os, threading, time, json


class SockAdapterClient:
    def __init__(self, PATH="/tmp/chat.sock"):
        self.path = PATH
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.connect(self.path)
        threading.Thread(target=self.receive, daemon=True).start()

    def send(self):
        """data format
        data = {
            "action": "api_call",
            "content": str,
            "opts":{tbd},
        }
        """
        data = {"action": "api_call", "content": "Who is ThePrimeAgen?", "opts": ""}
        data = json.dumps(data)
        print(data, "SENT")
        self.s.send(data.encode() + b"\n")

    def receive(self, ui_obj=None):
        while 1:
            data = self.s.recv(1024)
            # TODO
            if not data:
                break
            print(data)


c = SockAdapterClient()
c.send()
while 1:
    time.sleep(0.2)
