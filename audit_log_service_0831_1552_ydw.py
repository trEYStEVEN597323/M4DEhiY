# 代码生成时间: 2025-08-31 15:52:29
import logging
from datetime import datetime
from tornado.web import RequestHandler

# 配置日志
logging.basicConfig(filename='audit.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class AuditLogService:
    """安全审计日志服务，负责记录用户的请求和响应。"""

    @staticmethod
    def log_request(handler: RequestHandler, status_code: int):
        """记录请求日志。"""
        try:
            # 从handler获取请求信息
            request_info = {
                'ip': handler.request.remote_ip,
                'method': handler.request.method,
                'path': handler.request.path,
                'query': handler.request.query,
                'headers': dict(handler.request.headers),
                'body': handler.request.body.decode('utf-8'),
            }
            # 将请求信息和状态码记录到日志文件
            logging.info(f'Request: {request_info}, Status Code: {status_code}')
        except Exception as e:
            logging.error(f'Error logging request: {e}')

    def write_log(self, message: str):
        """将信息写入日志文件。"""
        try:
            logging.info(message)
        except Exception as e:
            logging.error(f'Error writing log: {e}')

class AuditLogHandler(RequestHandler):
    """处理请求并记录安全审计日志的Tornado请求处理器。"""

    def prepare(self):
        """请求处理前的准备工作。"""
        super().prepare()
        # 在请求处理前调用AuditLogService记录请求信息
        AuditLogService.log_request(self, 0)  # 0为占位符，实际状态码在write方法中记录

    def write(self, chunk):
        """写入响应内容。"""
        super().write(chunk)
        # 记录响应状态码
        AuditLogService.log_request(self, self.get_status())

    def on_finish(self):
        """请求处理完成后的清理工作。"""
        super().on_finish()
        # 记录请求完成信息
        AuditLogService().write_log(f'Request finished. Path: {self.request.path} Status: {self.get_status()}')