# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# Copyright 2013 Erin Torbiak
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import SocketServer
import os


class MyWebServer(SocketServer.BaseRequestHandler):
    def return_404(self):
        self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n404: Page Not Found")
        return
    
    def bad_path(self, root, reqpath):
        abs_root = os.path.abspath(root)
        abs_reqpath = os.path.abspath(reqpath)
        return not abs_reqpath.startswith(abs_root)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        # Parse input, remove leading slash
        lines = self.data.split("\r\n")
        first_line = lines[0].split()
        root = "./www"
        path = os.path.join(root, first_line[1][1:])

        # If directory given, return index
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")

        if not os.path.exists(path) or self.bad_path(root, path):
            self.return_404()
            return

        with open(path) as f:
            content = f.read()
        
        if path.endswith('.css'):
            response = "HTTP/1.1 200 OK\r\nContent-Type:text/css\r\n\r\n%s" % content
        elif path.endswith('.html'):
            response = "HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n%s" % content 
        self.request.sendall(response)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
