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
git_directory = "/root/applications/hexo/source"
delay_git = 2
delay_hexo = 20


def git_pull():
    os.system("cd  " + git_directory + " && git pull " + git_origins)
    # print("git pull")
    t = threading.Timer(delay_hexo, hexo_generate)
    t.start()


def hexo_generate():
    # print("hexo generate")
    os.system("hexo --cwd " + hexo_current_working_directory + " generate")


class myHandler(HTTP.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/update":
            print("com in post")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("OK", encoding="utf-8"))
            t = threading.Timer(delay_git, git_pull)
            t.start()
        return


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("com in")
    httpd.serve_forever()
