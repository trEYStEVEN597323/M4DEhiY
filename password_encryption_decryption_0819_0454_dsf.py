# 代码生成时间: 2025-08-19 04:54:13
import tornado.ioloop
import tornado.web
from cryptography.fernet import Fernet


class MainHandler(tornado.web.RequestHandler):
    """
    A Tornado RequestHandler that provides password encryption and decryption functionality.
    """
    def get(self):
        # Generates a key for encryption and decryption if it doesn't already exist.
        if not hasattr(self.application, 'fernet_key'):
            self.application.fernet_key = Fernet.generate_key()
        # Sets up the Fernet instance with the key.
        self.fernet = Fernet(self.application.fernet_key)

    def post(self):
        # Retrieve the password from the request body as a JSON object.
        try:
            data = self.get_json_body()
            password = data.get('password')
            if password is None:
                self.set_status(400)
                self.write({'error': 'Password is required'})
                return

            # Encrypt the password.
            encrypted_password = self.fernet.encrypt(password.encode()).decode()

            # Return the encrypted password.
            self.write({'encrypted_password': encrypted_password})
        except Exception as e:
            self.set_status(400)
            self.write({'error': str(e)})

    def put(self):
        # Retrieve the encrypted password from the request body as a JSON object.
        try:
            data = self.get_json_body()
            encrypted_password = data.get('encrypted_password')
            if encrypted_password is None:
                self.set_status(400)
                self.write({'error': 'Encrypted password is required'})
                return

            # Decrypt the password.
            password = self.fernet.decrypt(encrypted_password.encode()).decode()

            # Return the decrypted password.
            self.write({'password': password})
        except Exception as e:
            self.set_status(400)
            self.write({'error': str(e)})

    def get_json_body(self):
        """
        Retrieves JSON object from the request body.
        """
        try:
            return tornado.escape.json_decode(self.request.body)
        except Exception as e:
            self.set_status(400)
            self.write({'error': 'Invalid JSON format'})
            return None


def make_app():
    """
    Creates a Tornado application.
    """
    return tornado.web.Application([
        (r"/encrypt", MainHandler),
        (r"/decrypt", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Starting Tornado application on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
