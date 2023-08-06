import re
import sys


class Instruction:
    def __init__(self, ins_str):
        self.instruction = ins_str

    def is_valid(self):
        if self.instruction in INSTRUCTION_PATTERNS.keys():
            return True
        else:
            return False

    def get_function(self):
        pass

    def get_args(self):
        pass

    def execute(self):
        if INSTRUCTION_PATTERNS[self.instruction] == 'EXIT':
            sys.exit()
        else:
            print("execute an instruction")


INSTRUCTION_PATTERNS = {
    re.compile("quit", flags=re.I): 'EXIT',
    re.compile("q", flags=re.I): 'EXIT',
    re.compile("instruction", flags=re.I): 'INSTRUCTION'
}
