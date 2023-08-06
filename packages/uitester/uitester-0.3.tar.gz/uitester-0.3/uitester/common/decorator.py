from functools import wraps
import time
def timethis(func):
    """
    计时功能，计算一个函数运行所需的适合
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print("{:.2f}s".format(end-start))
        return result
    return wrapper