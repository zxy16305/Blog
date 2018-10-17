import http.server as HTTP
import socketserver
import os

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
        return


with socketserver.TCPServer(("", PORT), myHandler) as httpd:
    print("com in")
    httpd.serve_forever()
