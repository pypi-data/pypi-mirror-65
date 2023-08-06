from jiaowu.console.instruction import Instruction
from jiaowu.core.model.login_model import LoginInitializer
from jiaowu.core.model.spider_model import LoginSpider
from jiaowu.core.model.task_model import TaskExecutor, Task

instruction_buffer = []


def main():
    print("welcome to NJUjaowu helper system！\nplease login")
    username=input("Username:")
    pwd=input("Password:")
    initializer = LoginInitializer(username, pwd)
    cookie = initializer.start_session()
    spider = LoginSpider(cookie)
    task_executor=TaskExecutor(spider=spider)
    wait(task_executor=task_executor)


def wait(task_executor:TaskExecutor):
    end = False
    print("NJUjwc>>")
    instruction_str = input().strip()
    if instruction_str.endswith(';'):
        end = True
        instruction_str = instruction_str[0:-1]

    instruction = Instruction(instruction_str)
    if not instruction.is_valid():
        # rollback
        print("wrong instruction format,please enter [INSTRUCTION_NAME]? for help")
        wait(task_executor)
    else:
        task=instruction.to_task()
        task_executor.add_task(task)
        if end:
            task_executor.do_tasks()
        wait(task_executor)


