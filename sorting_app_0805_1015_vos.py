# 代码生成时间: 2025-08-05 10:15:15
import tornado.ioloop
import tornado.web

# Sorting algorithm class
class SortingAlgorithm:
    def __init__(self):
        pass

    # Bubble Sort
    def bubble_sort(self, arr):
        """
        Performs bubble sort on the given list.
        :param arr: List of elements to sort.
        :return: Sorted list.
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    # Insertion Sort
    def insertion_sort(self, arr):
        """
        Performs insertion sort on the given list.
        :param arr: List of elements to sort.
        :return: Sorted list.
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i-1
            while j >=0 and key < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
            arr[j+1] = key
        return arr

    # Selection Sort
    def selection_sort(self, arr):
        """
        Performs selection sort on the given list.
        :param arr: List of elements to sort.
        :return: Sorted list.
        """
        for i in range(len(arr)):
            min_idx = i
            for j in range(i+1, len(arr)):
                if arr[min_idx] > arr[j]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

# Tornado Application
class SortingHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            algorithm = SortingAlgorithm()
            numbers = [64, 34, 25, 12, 22, 11, 90]
            # Choose sorting method
            sorted_numbers = algorithm.bubble_sort(numbers)
            self.write({'status': 'success', 'sorted_numbers': sorted_numbers})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})

def make_app():
    return tornado.web.Application([
        (r"/", SortingHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server started on port 8888")
    tornado.ioloop.IOLoop.current().start()