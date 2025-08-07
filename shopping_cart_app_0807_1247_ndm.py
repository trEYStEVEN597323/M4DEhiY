# 代码生成时间: 2025-08-07 12:47:14
import tornado.ioloop
import tornado.web
from tornado.options import define, options

# 定义全局购物车对象
class ShoppingCart(dict):
    def add_product(self, product_id, quantity=1):
        """
        向购物车添加商品
        :param product_id: 商品ID
        :param quantity: 添加数量，默认为1
        """
        if product_id in self:
            self[product_id] += quantity
        else:
            self[product_id] = quantity
        return {'success': True, 'message': 'Product added to cart'}

    def remove_product(self, product_id, quantity=1):
        """
        从购物车移除商品
        :param product_id: 商品ID
        :param quantity: 移除数量，默认为1
        """
        if product_id in self:
            if self[product_id] > quantity:
                self[product_id] -= quantity
            else:
                del self[product_id]
            return {'success': True, 'message': 'Product removed from cart'}
        else:
            return {'success': False, 'message': 'Product not in cart'}

    def get_cart(self):
        """
        获取购物车中的商品列表
        """
        return {'success': True, 'message': 'Cart retrieved', 'cart': dict(self)}

# 定义路由和请求处理函数
class ShoppingCartHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.cart = ShoppingCart()

    def post(self):
        """
        添加商品到购物车
        """
        data = tornado.escape.json_decode(self.request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        if product_id:
            result = self.cart.add_product(product_id, quantity)
            self.write(result)
        else:
            self.set_status(400)
            self.write({'success': False, 'message': 'Product ID is required'})

    def delete(self):
        """
        从购物车移除商品
        """
        data = tornado.escape.json_decode(self.request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        if product_id:
            result = self.cart.remove_product(product_id, quantity)
            self.write(result)
        else:
            self.set_status(400)
            self.write({'success': False, 'message': 'Product ID is required'})

    def get(self):
        """
        获取购物车内容
        """
        result = self.cart.get_cart()
        self.write(result)

# 定义应用设置和路由
define('port', default=8888, help='run on the given port', type=int)

def make_app():
    return tornado.web.Application(
        [('/cart', ShoppingCartHandler)],
        **settings)

settings = {
    'debug': True,
}

if __name__ == '__main__':
    define.parse_command_line()
    app = make_app()
    app.listen(options.port)
    print(f'Shopping Cart App started on port {options.port}')
    tornado.ioloop.IOLoop.current().start()