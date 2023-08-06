import time

from src.core import Logger
from src.data.constants.status_code import StatusCode as Code


class StatusCodeLogger(Logger):
    def log(self, status_code: Code):
        print(status_code.get_msg())


class DiaryLogger(Logger):
    def log(self, msg):
        now=time.localtime()
        
        pass

