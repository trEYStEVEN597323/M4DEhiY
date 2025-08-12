# 代码生成时间: 2025-08-12 21:17:49
import psutil
import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application


class MemoryUsageHandler(RequestHandler):
    """
    Handler to analyze and return memory usage statistics.
    """
    def get(self):
        try:
            # Get memory usage details
            memory_stats = psutil.virtual_memory()

            # Create a response with memory usage data
            response = {
                "total": memory_stats.total,
                "available": memory_stats.available,
                "used": memory_stats.used,
                "free": memory_stats.free,
                "percentage": memory_stats.percent
            }
            self.write(json.dumps(response))
        except Exception as e:
            # Handle any exceptions that occur and return error message
            self.set_status(500)
            self.write(json.dumps({'error': str(e)}) )


def make_app():
    """
    Creates a Tornado application with the memory usage handler.
    """
    return Application(
        [
            (r"/memory", MemoryUsageHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on http://localhost:8888")
    IOLoop.current().start()
