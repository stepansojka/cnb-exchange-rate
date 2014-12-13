from six.moves.BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import codecs
import threading
import os

class FakeCNBHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            this_dir = os.path.dirname(os.path.abspath(__file__))
            p = os.path.join(this_dir, 'data') + self.path
            print(p)
            f = codecs.open(p, encoding='UTF-8')
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read().encode('UTF-8'))
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def start():
    server = HTTPServer(('127.0.0.1', 8080), FakeCNBHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    return server

