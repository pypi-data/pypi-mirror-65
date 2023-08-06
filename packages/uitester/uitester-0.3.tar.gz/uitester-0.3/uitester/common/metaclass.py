from .data import data

class Singleton(type):
    """
    单例类
    如果 data.is_quit == True 或者 第一次初始化，则返回新的实例
    否则 返回类的拷贝
    """
    def __init__(self, *args, **kwargs):

        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None or data.is_quit:
            data.is_quit = False
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance

        else:
            return self.__instance

