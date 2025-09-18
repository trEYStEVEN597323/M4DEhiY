# 代码生成时间: 2025-09-18 19:40:53
import tornado.ioloop
import tornado.web
import json
import numpy as np
import matplotlib.pyplot as plt

# 定义配置类，用于保存配置信息
class ChartConfig:
    def __init__(self):
        self.data = []
        self.options = {}

# 定义图表生成器类
class ChartGenerator:
    def __init__(self, config):
        self.config = config

    def generate_chart(self):
        """根据配置信息生成图表"""
        try:
            # 使用matplotlib生成图表
            plt.figure(figsize=(10, 6))
            plt.plot(self.config.data)
            plt.title(self.config.options.get("title", "Interactive Chart"))
            plt.xlabel(self.config.options.get("xlabel", "X-axis"))
            plt.ylabel(self.config.options.get("ylabel", "Y-axis"))
            plt.savefig("chart.png")
            return {"status": "success", "message": "Chart generated successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# 定义Tornado请求处理器
class ChartRequestHandler(tornado.web.RequestHandler):
    def post(self):
        """处理POST请求，生成图表"""
        try:
            # 解析请求数据
            data = json.loads(self.request.body)
            config = ChartConfig()
            config.data = data.get("data", [])
            config.options = data.get("options", {})

            # 生成图表
            chart_generator = ChartGenerator(config)
            result = chart_generator.generate_chart()

            # 返回结果
            self.write(json.dumps(result))
        except Exception as e:
            self.write(json.dumps({"status": "error", "message": str(e)}))

# 定义Tornado应用
class ChartApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/chart", ChartRequestHandler),
        ]
        super(ChartApp, self).__init__(handlers)

# 运行Tornado应用
if __name__ == "__main__":
    app = ChartApp()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()