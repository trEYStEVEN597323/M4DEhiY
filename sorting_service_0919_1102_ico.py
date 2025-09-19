# 代码生成时间: 2025-09-19 11:02:49
import tornado.ioloop
import tornado.web

"""
Sorting Service:
This service provides a simple interface for sorting numbers using different algorithms.
It is built using the Tornado framework for asynchronous networking.
"""

class SortingHandler(tornado.web.RequestHandler):
    """
    Request handler for sorting service.
    It handles GET requests with a query parameter 'numbers' which contains a string of numbers separated by commas.
    """
    def get(self):
        try:
            # Retrieve the query parameter 'numbers'
            numbers_str = self.get_query_argument('numbers', '')
            # Split the string into a list of numbers
            numbers = [int(num) for num in numbers_str.split(',')]
            # Sort the numbers
            sorted_numbers = self.sort_numbers(numbers)
            # Return the sorted list as a JSON response
            self.write({'sorted_numbers': sorted_numbers})
        except ValueError:
            # Handle the case where the input is not a valid list of numbers
            self.set_status(400)
            self.write({'error': 'Invalid input. Please provide a list of numbers separated by commas.'})
        except Exception as e:
            # Handle any other exceptions
            self.set_status(500)
            self.write({'error': str(e)})

    def sort_numbers(self, numbers):
        """
        Sorts the given list of numbers using the built-in sorted function.
        This is a simple and efficient way to sort numbers.
        """
        return sorted(numbers)

def make_app():
    """
    Creates a Tornado application with the sorting handler.
    """
    return tornado.web.Application([
        (r'/sort', SortingHandler),
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print("Sorting service started on port 8888")
    tornado.ioloop.IOLoop.current().start()