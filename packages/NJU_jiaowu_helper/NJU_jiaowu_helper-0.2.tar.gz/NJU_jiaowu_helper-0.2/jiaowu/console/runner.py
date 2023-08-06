from ..core.model.instruction_model import Instruction

instruction_buffer = []


def main():
    print("welcome to NJUjaowu helper system！")
    wait()


def wait():
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
        wait()
    else:
        if end:
            execute()
        else:
            wait()


def execute():
    for instruction in instruction_buffer:
        instruction.execute()
    wait()
