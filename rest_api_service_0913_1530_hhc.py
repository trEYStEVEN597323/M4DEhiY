# 代码生成时间: 2025-09-13 15:30:02
import tornado.ioloop
import tornado.web
import json

# 定义一个基本的RESTful API接口处理类
class MainHandler(tornado.web.RequestHandler):
    """
    主处理类，用于处理GET和POST请求。
    """
    def get(self):
        # 处理GET请求
        self.write("Hello, this is a GET request.")

    def post(self):
        # 处理POST请求
        try:
            data = json.loads(self.request.body)
            self.write(json.dumps({'status': 'success', 'message': 'Data received', 'data': data}))
        except json.JSONDecodeError:
            self.write(json.dumps({'status': 'error', 'message': 'Invalid JSON data'}))
            self.set_status(400)

# 设置路由，将URL路径和处理类绑定
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    # 创建应用实例
    app = make_app()
    # 监听8080端口
    app.listen(8080)
    # 启动IO循环，等待请求
    print("Server is running on http://localhost:8080")
    tornado.ioloop.IOLoop.current().start()