# 代码生成时间: 2025-08-10 06:09:39
import datetime
import schedule
import time
from tornado.ioloop import IOLoop
from tornado import gen

# 定义一个定时任务调度器类
class SchedulerService:
    """
    定时任务调度器
    """

    def __init__(self):
        self.jobs = []
        self.io_loop = IOLoop.current()

    def add_job(self, func, time):
        """
        添加定时任务

        :param func: 任务函数
        :param time: 执行时间
        """
        self.jobs.append((func, time))
        schedule.every().seconds(time).do(func)

    def start(self):
        """
        启动调度器
        """
        while True:
            schedule.run_pending()
            time.sleep(1)

    @gen.coroutine
    def run(self):
        """
        运行定时任务
        """
        try:
            self.start()
        except Exception as e:
            print(f"Error running scheduler: {e}")

# 示例任务函数
def job1():
    print(f"Job 1 executed at {datetime.datetime.now()}")

def job2():
    print(f"Job 2 executed at {datetime.datetime.now()}")

if __name__ == '__main__':
    # 创建调度器实例
    scheduler = SchedulerService()

    # 添加任务
    scheduler.add_job(job1, 10)
    scheduler.add_job(job2, 20)

    # 在 Tornado 的 IOLoop 中运行调度器
    scheduler.run()
    IOLoop.current().start()