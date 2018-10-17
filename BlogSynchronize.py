import http.server as HTTP
import socketserver
import os
import time
import threading
import logging

PORT = 15622
Protocol = "HTTP/1.1"
git_origins = "https://github.com/zxy16305/Blog"
hexo_current_working_directory = "/root/applications/hexo/"


class myHandler(HTTP.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/update":
            print("com in post")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("OK", encoding="utf-8"))
            os.system("git pull " + git_origins)
            t = threading.Timer(10, hexo_generate, args=())
            t.start()
        return


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("com in")
    httpd.serve_forever()


def hexo_generate():
    os.system("hexo --cwd " + hexo_current_working_directory + " generate")
