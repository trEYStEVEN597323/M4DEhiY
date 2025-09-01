# 代码生成时间: 2025-09-01 16:44:53
import tornado.ioloop
import tornado.web
import json
from tornado.options import define, options
import logging

# 定义程序配置参数
define('port', default=8888, help='port to run the server on', type=int)
define('debug', default=True, help='debug mode')

# 消息通知类
class NotificationService:
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        """
        添加消息到通知列表
        :param message: 消息内容
        """
        self.messages.append(message)
    
    def get_messages(self):
        """
        获取所有通知消息
        :return: 所有通知消息列表
        """
        return self.messages

# Tornado请求处理器
class NotificationHandler(tornado.web.RequestHandler):
    def initialize(self, notification_service):
        self.notification_service = notification_service
    
    def post(self):
        """
        接收POST请求，添加消息到通知系统
        """
        try:
            message = tornado.escape.json_decode(self.request.body)
            self.notification_service.add_message(message['text'])
            self.write({'status': 'success', 'message': 'Message added successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

    def get(self):
        """
        接收GET请求，获取所有通知消息
        """
        messages = self.notification_service.get_messages()
        self.write({'status': 'success', 'messages': messages})

# 设置路由和启动服务器
def make_app():
    notification_service = NotificationService()
    return tornado.web.Application([
        (r"/notifications", NotificationHandler, dict(notification_service=notification_service)),
    ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    logging.info(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()
