# 代码生成时间: 2025-09-04 01:52:54
import os
import psutil
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

# SystemPerformanceMonitorHandler handles requests to monitor system performance
class SystemPerformanceMonitorHandler(RequestHandler):
    def get(self):
        try:
            # Collecting CPU, memory, and disk usage statistics
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            # Creating a response with system performance data
            response = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage
            }
            self.write(response)
        except Exception as e:
            # Error handling
            self.set_status(500)
            self.write({'error': str(e)})

# Application setup
def make_app():
    return Application(
        [(r"/monitor", SystemPerformanceMonitorHandler)],
        debug=True
    )

# Run the application
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("System Performance Monitor started on http://localhost:8888/monitor")
    IOLoop.current().start()

# Note: This script requires the psutil library to be installed.
#       You can install it using pip: pip install psutil