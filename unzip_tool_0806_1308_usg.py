# 代码生成时间: 2025-08-06 13:08:16
import os
import zipfile
import tornado.web
import tornado.ioloop
from tornado.options import define, options

# 定义命令行参数
define('port', default=8888, help='run on the given port', type=int)

class UnzipHandler(tornado.web.RequestHandler):
    """处理压缩文件解压的请求。"""
    def get(self):
        # 获取文件名参数
        filename = self.get_query_argument('filename')
        if not filename:
            self.write('No filename provided.')
            return

        # 检查文件名是否合法
        if '..' in filename or filename.startswith('/'):
            self.write('Invalid filename.')
            return

        # 构造完整的文件路径
        file_path = os.path.join(options.static_path, filename)

        try:
            # 创建解压目录
            extract_path = os.path.splitext(file_path)[0]
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)

            # 解压文件
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            self.write(f'File {filename} has been extracted successfully to {extract_path}')
        except zipfile.BadZipFile:
            self.write('Invalid zip file.')
        except Exception as e:
            self.write(f'An error occurred: {e}')

class UnzipApplication(tornado.web.Application):
    """创建Tornado应用程序。"""
    def __init__(self):
        handlers = [
            (r"/unzip", UnzipHandler),
        ]
        super().__init__(handlers)

    def start(self):
        """启动Tornado应用程序。"""
        print(f'Starting server on port {options.port}')
        self.listen(options.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    # 解析命令行参数
    tornado.options.parse_command_line()

    # 创建并启动应用程序
    UnzipApplication().start()