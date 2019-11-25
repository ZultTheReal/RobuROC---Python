import threading
import http.server
import socketserver

class ThreadedHTTPServer(object):

    def __init__(self, host, port, request_handler=http.server.SimpleHTTPRequestHandler):

        self.server = socketserver.TCPServer( (host, port), request_handler )
        
        self.thread = threading.Thread( target=self.server.serve_forever )
        print("Webserver started at http://localhost:" + str(port))

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

# Start the threaded server
server = ThreadedHTTPServer("0.0.0.0", 8080)
server.start()
