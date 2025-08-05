# 代码生成时间: 2025-08-06 02:27:24
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import json

# 定义全局购物车数据
shopping_cart = {}

# 设置全局变量
define("port", default=8888, help="run on the given port", type=int)

class ShoppingHandler(tornado.web.RequestHandler):
    # 获取购物车数据
    def get(self):
        cart_id = self.get_argument("id")
        if cart_id in shopping_cart:
            self.write(shopping_cart[cart_id])
        else:
            self.write({"error": "Cart not found"})
            self.set_status(404)
    
    # 添加商品到购物车
    def post(self):
        args = self.request.arguments
        if len(args) == 0:
            self.write({"error": "No items in request"})
            self.set_status(400)
            return
        
        cart_id = args.get("id", [None])[0]
        if cart_id is None:
            self.write({"error": "Cart ID is required"})
            self.set_status(400)
            return
        
        if cart_id not in shopping_cart:
            shopping_cart[cart_id] = []
        
        items = []
        for key, value in args:
            if key != "id":
                items.append({"item": key, "quantity": int(value[0])})
        
        shopping_cart[cart_id].extend(items)
        self.write(shopping_cart[cart_id])
    
    # 更新购物车中的商品数量
    def put(self):
        args = self.request.arguments
        if len(args) < 2:
            self.write({"error": "Item and quantity are required"})
            self.set_status(400)
            return
        
        cart_id = args.get("id", [None])[0]
        if cart_id is None or cart_id not in shopping_cart:
            self.write({"error": "Cart ID is invalid or not found"})
            self.set_status(404)
            return
        
        item = args.get("item", [None])[0]
        quantity = int(args.get("quantity", ["0"])[0])
        if item is None:
            self.write({"error": "Item is required"})
            self.set_status(400)
            return
        
        updated_cart = [item_info for item_info in shopping_cart[cart_id] if item_info["item"] != item]
        updated_cart.append({"item": item, "quantity": quantity})
        shopping_cart[cart_id] = updated_cart
        self.write(shopping_cart[cart_id])
    
    # 从购物车中移除商品
    def delete(self, item_id):
        cart_id = self.get_argument("id")
        if cart_id not in shopping_cart:
            self.write({"error": "Cart not found"})
            self.set_status(404)
            return
        
        if item_id in shopping_cart[cart_id]:
            shopping_cart[cart_id].remove(item_id)
            self.write(shopping_cart[cart_id])
        else:
            self.write({"error": "Item not found in cart"})
            self.set_status(404)
    
# 应用设置
application = tornado.web.Application([
    (r"/cart", ShoppingHandler),
], debug=True)

if __name__ == "__main__":
    options.parse_command_line()
    application.listen(options.port)
    print(f"Server is running on http://localhost:{options.port}")
    tornado.ioloop.IOLoop.current().start()