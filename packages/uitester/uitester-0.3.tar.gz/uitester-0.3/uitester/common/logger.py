import logging
import sys
import os
class Logger(object):

    def __init__(self,logname,stream_level="info",file_level="debug"):
        self.logname = logname
        self.logger = logging.getLogger(logname)
        self.logger.setLevel(level=logging.DEBUG)
        self.add_stream_hander(stream_level)
        self.add_file_hander(file_level)
        self.add_method()

    def get_level(self,level):
        if level == "info":
            return logging.INFO
        elif level == "debug":
            return logging.DEBUG
        elif level == "warning":
            return logging.WARNING

    def add_method(self):
        self.info = self.logger.info
        self.debug = self.logger.debug
        self.warning = self.logger.warning
        self.error = self.logger.error

    def add_stream_hander(self,level):
        level = self.get_level(level)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level=level)
        self.logger.addHandler(stream_handler)

    def add_file_hander(self,level):
        if not os.path.exists('log'):
            os.mkdir('log')
        level = self.get_level(level)
        file_handler = logging.FileHandler('log/{}.log'.format(self.logname))
        file_handler.setLevel(level=level)
        formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

if __name__ == '__main__':
    logger  = Logger("gui")
    logger.info("hello")
    logger.warning("hello")