# 代码生成时间: 2025-09-08 17:03:44
import tornado.ioloop
import tornado.web
import tornado.gen
from urllib.parse import urlparse
from tornado.httpclient import AsyncHTTPClient, HTTPError

class UrlValidatorHandler(tornado.web.RequestHandler):
    """
    Handles URL validation requests.
    """
    @tornado.gen.coroutine
    def get(self, url):
        """
        Validates the provided URL.
        """
        try:
            # Parse the URL to ensure it is in the correct format
            parsed_url = urlparse(url)
            if not all([parsed_url.scheme, parsed_url.netloc]):
                self.write("Invalid URL provided.")
                self.set_status(400)
                return

            # Create an HTTP client
            http_client = AsyncHTTPClient()
            # Fetch the URL to check its validity
            response = yield http_client.fetch(url)
            # If the response is successful, the URL is valid
            self.write(f"URL {url} is valid.")
        except HTTPError as e:
            # Handle HTTP errors (e.g., invalid URL, connection timeouts)
            self.write(f"HTTP error: {e} - URL {url} is invalid.")
            self.set_status(e.code)
        except Exception as e:
            # Handle other exceptions (e.g., parsing errors)
            self.write(f"Error: {e} - URL {url} is invalid.")
            self.set_status(500)

def make_app():
    """
    Creates the Tornado application.
    """
    return tornado.web.Application(
        handlers=[(r"/validate/([^\/]+)",
                    UrlValidatorHandler)],
        debug=True,
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()