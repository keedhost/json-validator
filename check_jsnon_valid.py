#!/usr/bin/python3

"""
Very simple HTTP server in python for logging and checking requests
Usage:
    ./check_jsnon_valid.py [<port>]


Password for cert: [unable to show the password]
Cert generated using command:
$ openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 
for server with IP 172.24.201.82
Check valid JSON:
$ curl -s -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -X POST -k https://172.24.201.82:5000 -v
Check invalid JSON:
$ curl -s -d "{'age':100 }" -H "Content-Type: application/json" -X POST -k https://172.24.201.82:5000 -v

"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import logging
import json

SECURED = False

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f'\n\nHeaders:\n{str(self.headers)}')
        #self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info(f"\n\nHeaders:\n{str(self.headers)}\nBody:\n{post_data.decode('utf-8')}\n")
        
        if is_json(post_data.decode('utf-8')):
        	print('\033[92m\033[1mJSON is valid\033[0m')
        	self.send_response(200)
        else:
        	print('\033[91m\033[1mJSON is NOT valid\033[0m')
        	self.send_response(500)

        #self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        print('-' * 80)

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    if SECURED:
    	httpd.socket = ssl.wrap_socket (httpd.socket, keyfile="./cert/key.pem", certfile='./cert/cert.pem', server_side=True)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
