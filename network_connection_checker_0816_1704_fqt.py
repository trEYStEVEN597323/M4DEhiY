# 代码生成时间: 2025-08-16 17:04:56
import tornado.ioloop
import tornado.web
import socket
from urllib.parse import urlparse

"""
Network Connection Checker using Python and Tornado framework.
This application provides a simple API endpoint to check the network connection status.
"""

class ConnectionHandler(tornado.web.RequestHandler):
    """
    A Tornado RequestHandler to check the network connection status.
    It takes a URL as input and checks if the connection is successful.
    """
    def get(self):
        # Get the URL from the query parameter
        url = self.get_query_argument('url')
        try:
            # Parse the URL to extract the domain
            domain = urlparse(url).netloc
            # Use socket to check if the domain is reachable
            sock = socket.create_connection((domain, 80), timeout=5)
            self.write({'status': 'success', 'message': 'Connection established.'})
        except (socket.error, socket.timeout) as e:
            # Handle connection errors
            self.set_status(404)
            self.write({'status': 'error', 'message': 'Failed to establish connection.', 'error': str(e)})
        finally:
            # Properly close the socket connection
            if 'sock' in locals():
                sock.close()

class Application(tornado.web.Application):
    """
    A Tornado Application with a single endpoint for checking network connections.
    """
    def __init__(self):
        handlers = [(r'/', ConnectionHandler)]
        super(Application, self).__init__(handlers)

if __name__ == '__main__':
    # Create the application instance
    app = Application()
    # Start the IOLoop to listen for requests
    tornado.ioloop.IOLoop.current().start()
