# 代码生成时间: 2025-09-01 02:54:59
import os
from PIL import Image
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line

# 定义全局变量
define("port", default=8888, help="run on the given port", type=int)

# 图片尺寸批量调整器类
class ImageResizer:
# 改进用户体验
    def __init__(self, resize_width, resize_height):
        self.resize_width = resize_width
        self.resize_height = resize_height
# TODO: 优化性能

    def resize_image(self, image_path):
        """Resize a single image.

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: The path to the resized image file.
        """
# NOTE: 重要实现细节
        try:
            with Image.open(image_path) as img:
                # Resize the image
                resized_img = img.resize((self.resize_width, self.resize_height))
                # Save the resized image
                os.remove(image_path)  # Remove the original image
                resized_img.save(image_path)
                return image_path
        except IOError:
# 增强安全性
            # Handle errors for non-image files
            print(f"Error: {image_path} is not a valid image file.")
            return None

    def resize_images(self, directory):
        """Resize all images in a directory.

        Args:
            directory (str): The path to the directory containing images.
        """
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
# 优化算法效率
                image_path = os.path.join(directory, filename)
                self.resize_image(image_path)

# Tornado 请求处理类
class MainHandler(RequestHandler):
    def get(self):
# TODO: 优化性能
        self.write("Image Resizer API is running...")

    def post(self):
# 添加错误处理
        # 获取请求参数
# 改进用户体验
        directory = self.get_query_argument("directory")
        resize_width = int(self.get_query_argument("width"))
# 增强安全性
        resize_height = int(self.get_query_argument("height"))

        # 调用图片尺寸批量调整器
# 扩展功能模块
        resizer = ImageResizer(resize_width, resize_height)
        resizer.resize_images(directory)

        self.write("Images have been resized successfully.")
# 优化算法效率

# 创建 Tornado 应用
def make_app():
    return Application([
        (r"/", MainHandler),
    ])

# 运行服务器
if __name__ == "__main__":
    parse_command_line()
    app = make_app()
# 扩展功能模块
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().start()