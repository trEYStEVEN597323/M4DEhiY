# 代码生成时间: 2025-08-05 16:25:46
import os
from PIL import Image
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, HTTPError

# 图片尺寸批量调整器
class ImageResizerHandler(RequestHandler):
    def post(self):
        # 获取上传的图片和目标尺寸
        uploaded_file = self.request.files['image'][0]
        target_width = self.get_argument('width', None)
        target_height = self.get_argument('height', None)

        if not target_width or not target_height:
            raise HTTPError(400, 'Width and height must be provided.')

        try:
            image_data = uploaded_file.body
            image = Image.open(BytesIO(image_data))
        except Exception as e:
            raise HTTPError(400, f'Invalid image: {e}')

        # 调整图片尺寸
        resized_image = image.resize((int(target_width), int(target_height)), Image.ANTIALIAS)

        # 保存并返回图片
        output_buffer = BytesIO()
        resized_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)

        self.set_header('Content-Type', 'image/jpeg')
        self.write(output_buffer.read())

# 设置路由和启动Tornado服务器
def make_app():
    return Application([
        (r"/resize", ImageResizerHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()

# 注意：本示例代码中使用了Pillow库进行图片处理，请确保已安装相关依赖。
#       pip install Pillow tornado
