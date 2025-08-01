# 代码生成时间: 2025-08-02 01:03:38
import tornado.ioloop
import tornado.web
from tornado.options import define, options
from tornado.web import RequestHandler
from functools import wraps
import bcrypt
import json

# 配置选项
define("port", default=8888, help="run on the given port", type=int)

# 假设的用户数据库（实际应用中应使用数据库存储）
users = {
    "user1": bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    "user2": bcrypt.hashpw("password2".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
}

# 用户认证装饰器
def authenticate(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        self.current_user = None
        token = self.get_secure_cookie("user")
        if token:
            self.current_user = self.get_auth_user(token)
        return await func(self, *args, **kwargs)
    return wrapper

# 获取授权用户
def get_auth_user(token):
    return users.get(token)

# 身份验证处理器
class AuthHandler(RequestHandler):
    @authenticate
    def get(self):
        self.write("Welcome, {}".format(self.current_user))

class LoginHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        username = data.get("username")
        password = data.get("password")
        user = users.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.encode('utf-8')):
            token = bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            self.set_secure_cookie("user", token)
            self.write("User logged in")
        else:
            self.set_status(401)
            self.write("Authentication failed")

class LogoutHandler(RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("User logged out")

# 设置路由
def make_app():
    return tornado.web.Application(
        [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/", AuthHandler),
        ],
        cookie_secret="your_secret_key",
        login_url="/login"
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print("Server is running on port: " + str(options.port))
    tornado.ioloop.IOLoop.current().start()