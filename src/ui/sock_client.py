import json
import os
import socket
import threading
import time
from json import JSONDecodeError


class SockAdapterClient:
    def __init__(self, textual_obj, PATH="/tmp/chat.sock"):
        self.textual_obj = textual_obj
        self.path = PATH
        self.buffer = ""
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.connect(self.path)
        threading.Thread(target=self.receive, daemon=True).start()

    def send(self, prompt):
        """ data format will be
            data = {"action": "api_call", "content": str, "opts":{tbd},}
        """
        data = {"action": "api_call", "content": f"{prompt}", "opts": ""}
        data = json.dumps(data)
        self.s.send(data.encode() + b"\n")

    def receive(self):
        while 1:
            data = self.s.recv(4096).decode()
            if not data:
                break

            self.buffer += data

            while "\n" in self.buffer:
                line, self.buffer = self.buffer.split("\n", 1)

                if not line.strip():
                    continue
                try:
                    delta = json.loads(line)
                except JSONDecodeError as e:
                    delta = None

                """ delta format will be
                # delta = { content,role,reasoning,reasoning_details }
                """
                if delta:
                    if delta.get("content") and delta.get("role"):
                        self.textual_obj.stream_response(delta.get("content"))
