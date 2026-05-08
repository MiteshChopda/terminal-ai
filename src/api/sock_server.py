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
        self.running = True
        self.CONN = None

    def start(self):
        print("Server listening...")
        while self.running:
            conn, _ = self.s.accept()
            print("Client connected")
            self.CONN = conn
            threading.Thread(
                target=self.recv_loop,
                args=(),
                daemon=True
            ).start()


    def send(self, msg):
        # expect string and not encoded data
        print("\nSENT :", msg)
        if self.CONN:
            # '\n' mandatory for client parsing data
            self.CONN.sendall((msg + '\n').encode())
            return True
        else:
            return False

    def recv_loop(self):
        while 1:
            data = self.CONN.recv(4096)
            if not data:
                break
            print("DATA RECIEVED:", data.decode())
            data_list = data.decode().split("\n")

            for i, data in enumerate(data_list):
                print(f"DATA of {i}:", data)
                if not data:
                    continue
                data = json.loads(data)
                """ data format
                    data = { "action": "api_call","content": str, "opts":{tbd}}
                """
                if data.get("action") == "api_call":
                    # call
                    if data.get("content"):
                        api_call(self, prompt=data.get("content"))

if __name__ == "__main__":
    s = SockAdapter()
    s.start()
