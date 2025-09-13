# 代码生成时间: 2025-09-13 20:41:31
import requests
from bs4 import BeautifulSoup
import tornado.ioloop
import tornado.web

"""
A simple Tornado web application to fetch and display web content.
This script is designed to be a basic web content grabber,
fetching content from a given URL and displaying it.
"""

class FetchHandler(tornado.web.RequestHandler):
    """
    Request handler to fetch and display web content.
    """
    def get(self):
        url = self.get_argument('url')
        try:
            # Fetch the content from the given URL
            response = requests.get(url)
            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Get the text content of the page
            content = soup.get_text()

            # Display the fetched content
            self.write(content)
        except requests.RequestException as e:
            # Handle any request-related errors
            self.write(f'Error fetching content: {e}')
        except Exception as e:
            # Handle any other errors
            self.write(f'An error occurred: {e}')

class Application(tornado.web.Application):
    """
    Tornado application class.
    """
    def __init__(self):
        handlers = [
            (r'/fetch', FetchHandler),
        ]
        super(Application, self).__init__(handlers)

def make_app():
    """
    Function to create the Tornado application.
    """
    return Application()

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('Web content grabber server is running on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()