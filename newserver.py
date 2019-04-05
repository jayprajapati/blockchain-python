from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socketserver
from urllib.parse import urlparse
from block import *
HTTP_STARTED=False
# HTTPRequestHandler class
mbc=blockchain(name='j',node="1923168686",port="2158")
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        parsed_path = urlparse(self.path)
        self.end_headers()
        
  def do_HEAD(self):
    self._set_headers()
        
  def do_GET(self):
        self._set_headers()
        
        
        self.wfile.write(json.dumps(mbc.get_json()).encode("utf-8"))
        return
 
def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('127.0.0.1', 8081)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()
  #httpd.server_close
 

