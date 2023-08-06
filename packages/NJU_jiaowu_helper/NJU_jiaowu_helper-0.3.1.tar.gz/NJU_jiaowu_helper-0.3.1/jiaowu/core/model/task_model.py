from queue import Queue

from jiaowu.core.model.spider_model import LoginSpider


class TEMeta(type):
    def __new__(mcs, class_name, class_parents, class_attr):
        # 为任务执行类创建一个任务队列和消息队列
        class_attr["__task_queue"] = Queue()
        class_attr["__msg_queue"] = Queue()
        return super().__new__(mcs, class_name, class_parents, class_attr)


class TaskExecutor(metaclass=TEMeta):
    """
    任务执行类
    """
    __task_queue: Queue
    __msg_queue: Queue
    spider: LoginSpider

    def __init__(self, spider):
        self.spider = spider

    def add_task(self, task):
        # 向任务队列中添加任务
        self.__task_queue.put(task)
        return self

    def __do_task(self):
        # 执行下一个任务
        if not self.__task_queue.empty():
            task = self.__task_queue.get()
            task.do_task(self.__msg_queue, self.spider)
            self.__task_queue.task_done()
        else:
            print("任务队列为空，无可执行任务")

        return self

    def do_tasks(self):
        # 执行所有任务
        pointer = self
        for i in range(self.__task_queue.qsize()):
            pointer = pointer.__task_queue.get().__do_task()
        return pointer

    def remove_all_tasks(self):
        # 清除剩余任务
        self.__task_queue.empty()
        return self


class Task:
    TASK_NUM = None  # 任务编号
    TASK_ARGS = None  # 任务参数

    def __init__(self, task_function, args):
        self.function_pointer = task_function
        self.args = args

    def do_task(self, msg_queue: Queue, spider: LoginSpider):
        # 执行自身
        result = self.function_pointer(spider, self.args)
        # download functions
        if result is not None:
            msg_queue.put(result)
