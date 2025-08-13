# 代码生成时间: 2025-08-13 09:26:18
import tornado.ioloop
import tornado.web
import requests
from bs4 import BeautifulSoup
import urllib.parse
def scrape_content(url):
    """
    Scrapes the content of a webpage given a URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        str: The content of the webpage or an error message if scraping fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code.
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
def make_app():
    """
    Creates a Tornado web application with a single route to handle scraping requests.
    """
    return tornado.web.Application([
        (r"/scrape", ScrapeHandler),
    ])
def main():
    """
    Initializes the Tornado web server and starts the IO loop.
    """
    app = make_app()
    app.listen(8888)
    print("Web Content Scraper server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()class ScrapeHandler(tornado.web.RequestHandler):
    """
    A Tornado RequestHandler that scrapes content from a given URL.
    """
    @tornado.web.asynchronous
    def post(self):
        """
        Handles POST requests to the /scrape endpoint.
        """
        url = self.get_argument("url")
        content = scrape_content(url)
        self.write({"status": "success", "content": content})
        self.finish()if __name__ == "__main__":
    main()