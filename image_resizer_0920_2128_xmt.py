# 代码生成时间: 2025-09-20 21:28:19
import os
from PIL import Image
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.escape import json_encode, json_decode

# 图片尺寸批量调整器
class ImageResizerHandler(RequestHandler):
    def post(self):
        # 获取上传的文件列表
        files = self.request.files.get('images', [])
        if not files:
            self.write({'error': 'No images provided.'})
            return

        # 获取目标尺寸
        target_width = self.get_argument('width', 0)
        target_height = self.get_argument('height', 0)
        if target_width == 0 or target_height == 0:
            self.write({'error': 'Invalid dimensions.'})
            return

        # 调整尺寸并保存图片
        resized_images = []
        for file in files:
            try:
                # 打开图片
                image = Image.open(file['body'])

                # 调整尺寸
                image = image.resize((target_width, target_height), Image.ANTIALIAS)

                # 保存图片
                image.save(file['filename'])
                resized_images.append(file['filename'])
            except Exception as e:
                # 错误处理
                self.write({'error': str(e)})
                return

        # 返回结果
        self.write({'resized_images': resized_images})

# 设置Tornado应用
def make_app():
    return Application(
        [
            (r'/resize', ImageResizerHandler),
        ],
        debug=True,
    )

if __name__ == '__main__':
    app = make_app()
    http_server = HTTPServer(app)
    http_server.listen(8888)
    IOLoop.current().start()

"""
Image Resizer API

A simple API to resize images in batch.

POST /resize
- images: A list of image files to resize.
- width: The target width for the resized images.
- height: The target height for the resized images.

Returns a JSON object with the resized images' filenames.

Example:
POST /resize
- images: file1.jpg, file2.jpg
- width: 800
- height: 600

Response: {"resized_images": ["file1.jpg", "file2.jpg"]}
"""