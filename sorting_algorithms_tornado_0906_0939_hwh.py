# 代码生成时间: 2025-09-06 09:39:49
import tornado.ioloop
import tornado.web

# 排序算法实现类
class SortingAlgorithms:
    def __init__(self):
        pass

    # 冒泡排序
    def bubble_sort(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    # 插入排序
    def insertion_sort(self, arr):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    # 选择排序
    def selection_sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

# Tornado 路由处理器
class SortHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            # 获取查询参数
            arr = self.get_query_argument('arr', default="")
            if arr == "" or not arr:
                raise ValueError("Array parameter is missing or empty.")
            arr = list(map(int, arr.split(',')))
            sorting_algorithm = SortingAlgorithms()
            # 根据不同的排序算法进行排序
            sort_type = self.get_query_argument('sort', 'bubble')
            if sort_type == 'bubble':
                sorted_arr = sorting_algorithm.bubble_sort(arr)
            elif sort_type == 'insertion':
                sorted_arr = sorting_algorithm.insertion_sort(arr)
            elif sort_type == 'selection':
                sorted_arr = sorting_algorithm.selection_sort(arr)
            else:
                raise ValueError("Invalid sorting algorithm.")
            # 返回排序结果
            self.write({'sorted_arr': sorted_arr})
        except Exception as e:
            self.write({'error': str(e)})

# 应用设置
application = tornado.web.Application([
    (r"/sort", SortHandler),
])

if __name__ == "__main__":
    # 运行Tornado服务器
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()