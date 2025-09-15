# 代码生成时间: 2025-09-16 02:20:04
import tornado.ioloop
import tornado.web
import hashlib
import base64

"""
哈希值计算工具 - 一个使用Tornado框架的Web服务
提供哈希值计算功能，支持SHA256和MD5算法。

使用方法：
1. 启动服务：运行python hash_calculator.py
2. 访问服务：在浏览器中输入 http://localhost:8888/ ，
   输入要计算哈希值的文本，选择哈希算法，提交表单。
"""

class MainHandler(tornado.web.RequestHandler):
    """
    主处理器，处理哈希值计算请求。
    """
    def get(self):
        # 提供一个HTML表单供用户提交数据
        self.write("""
        <form action="/calculate" method="post">
            <input type="text" name="text" placeholder="Enter text here..." required>
            <select name="algorithm">
                <option value="sha256">SHA256</option>
                <option value="md5">MD5</option>
            </select>
            <input type="submit" value="Calculate Hash">
        </form>
        