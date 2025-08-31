# 代码生成时间: 2025-08-31 09:50:59
import tornado.ioloop
import tornado.web
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
性能测试脚本，使用Tornado框架和requests库对目标网站进行性能测试。
该脚本使用ThreadPoolExecutor来并发发送HTTP请求，并统计响应时间。
"""

class PerformanceTestHandler(tornado.web.RequestHandler):
    """
    Tornado请求处理器，用于性能测试。
    """
    def get(self):
        # 获取URL参数
        url = self.get_query_argument('url')
        num_requests = int(self.get_query_argument('num_requests', '1'))
        concurrency = int(self.get_query_argument('concurrency', '1'))
        
        # 执行性能测试
        start_time = time.time()
        results = perform_load_test(url, num_requests, concurrency)
        end_time = time.time()
        
        # 计算总耗时
        elapsed_time = end_time - start_time
        self.write(
            f"Total Time: {elapsed_time:.2f} seconds, "
            f"Average Response Time: {sum(results) / len(results):.2f} seconds"
        )


def perform_load_test(url, num_requests, concurrency):
    """
    执行性能测试
    
    :param url: 目标URL
    :param num_requests: 请求总数
    :param concurrency: 并发数
    :return: 响应时间列表
    """
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        # 提交请求任务
        future_to_url = {executor.submit(make_request, url): url for _ in range(num_requests)}
        
        # 获取结果
        for future in as_completed(future_to_url):
            try:
                response_time = future.result()
                results.append(response_time)
            except Exception as exc:
                print(f"Request generated an exception: {exc} - {future_to_url[future]}")
    return results


def make_request(url):
    """
    发送单个HTTP请求并返回响应时间
    
    :param url: 目标URL
    :return: 响应时间（秒）
    """
    start_time = time.time()
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise e
    return time.time() - start_time


def make_app():
    """
    创建Tornado应用
    """
    return tornado.web.Application([
        (r"/perform_test", PerformanceTestHandler),
    ])


def main():
    """
    程序入口点
    """
    app = make_app()
    app.listen(8888)
    print("Starting Tornado server on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()