import cnb_exchange_rate as cnb

from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import codecs
import threading
import os

PORT = 8991
ENCODING = 'UTF-8'

class FakeCNBHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            this_dir = os.path.dirname(os.path.abspath(__file__))
            p = os.path.join(this_dir, 'data') + self.path
            print(p)
            f = codecs.open(p, encoding=ENCODING)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read().encode(ENCODING))
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def start():
    cnb.set_host('127.0.0.1:%d' % PORT)
    server = HTTPServer(('127.0.0.1', PORT), FakeCNBHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    return server

