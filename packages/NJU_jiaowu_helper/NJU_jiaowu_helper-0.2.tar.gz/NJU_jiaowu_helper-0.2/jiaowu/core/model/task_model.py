from queue import Queue

from jiaowu.data.constants.tasks_reflection import TASKNAME


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

    def __init__(self, spider):
        self.spider = spider

    def add_task(self, task_name: TASKNAME, args):
        # 向任务队列中添加任务
        task_function = task_name.value
        task = Task(task_function, args)
        self.__task_queue.put(task)
        return self

    def do_task(self):
        # 执行下一个任务

        return self

    def do_tasks(self):
        # 执行所有任务
        pass

    def remove_all_tasks(self):
        # 清除剩余任务
        self.__task_queue.empty()


class Task:
    TASK_NUM = None  # 任务编号
    TASK_ARGS = None  # 任务参数

    def __init__(self, task_function, args):
        pass

    def do_task(self):
        # 执行自身
        pass
