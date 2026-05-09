from http.server import BaseHTTPRequestHandler, HTTPServer
import time, random

class StreamHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()
        choose_response = [1, 2, 3, 4, 5]
        with open(f"streamresponse{random.choice(choose_response)}", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break  # Stop when end of file is reached
                print(line.strip())

                line = line.encode()
                # send chunk size in hex
                self.wfile.write(f"{len(line):X}\r\n".encode())
                self.wfile.write(line)
                self.wfile.write(b"\r\n")

                self.wfile.flush()
        # end stream
        self.wfile.write(b"0\r\n\r\n")
        self.wfile.flush()

server = HTTPServer(("0.0.0.0", 8000), StreamHandler)
print("Serving on :8000")
server.serve_forever()
