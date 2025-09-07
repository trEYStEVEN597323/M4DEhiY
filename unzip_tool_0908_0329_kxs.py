# 代码生成时间: 2025-09-08 03:29:38
import os
import zipfile
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler

# Define command line options
define("input_file", type=str, help="Path to the zip file", required=True)
define("output_dir", type=str, help="Directory to extract the zip file", required=True)

class UnzipHandler(RequestHandler):
    """
    Handler to handle unzip requests.
    """
    async def post(self):
        try:
            # Get input file and output directory from options
            input_file = options.input_file
            output_dir = options.output_dir

            # Check if the file exists
            if not os.path.isfile(input_file):
                self.write("Input file does not exist")
                self.set_status(404)
                return

            # Check if the directory exists
            if not os.path.isdir(output_dir):
                self.write("Output directory does not exist")
                self.set_status(404)
                return

            # Unzip the file
            with zipfile.ZipFile(input_file, 'r') as zip_ref:
                zip_ref.extractall(output_dir)

            # Return success message
            self.write("File has been successfully extracted")
            self.set_status(200)

        except zipfile.BadZipFile:
            self.write("Invalid zip file")
            self.set_status(400)
        except Exception as e:
            self.write(f"An error occurred: {str(e)}")
            self.set_status(500)

def make_app():
    """
    Create a Tornado application.
    """
    return tornado.web.Application(
        [
            (r"/unzip", UnzipHandler),
        ],
    )

if __name__ == "__main__":
    # Parse command line options
    tornado.options.parse_command_line()

    # Create the application
    app = make_app()

    # Start the IOLoop and listen on port 8888
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()