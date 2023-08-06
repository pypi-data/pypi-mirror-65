"""
为Task提供接口
"""
import re
from jiaowu.core.model.task_model import Task
from jiaowu.data.constants.tasks_reflection import TASK_LIST, PARAM_LIST


class Instruction:
    header = None
    function_abbr = None
    ins_str = None
    params = {}

    def __init__(self, ins_str):
        self.ins_str = ins_str
        self.__analyze_header()
        self.__analyze_param()

    def __analyze_header(self):
        self.header = self.ins_str.strip().split()[0]

    def __analyze_param(self):
        parts = self.ins_str.strip().split()
        for i in range(len(parts)):
            result = re.match("-(\d+)", parts[i])
            if result:
                if i + 1 < len(parts):
                    self.params[result.group(1)] = parts[i + 1]
                else:
                    self.params[result.group(1)] = None

    def is_valid(self):
        if self.header not in [x.split()[0] for x in INSTRUCTION_PATTERNS.keys()]:
            return False
        instruction_pattern = None
        for ele in INSTRUCTION_PATTERNS.items():
            if ele[0].split()[0] == self.header:
                instruction_pattern = ele[0]
                self.function_abbr = ele[1]
        flag = True
        param_pattern = {}
        s = instruction_pattern[0].split()[1]
        s = s[6:len(s) - 1]
        for x in s.split(';'):
            param_pattern[x.split(':')[0]] = x.split(':')[1]
        # 检测参数是否合法
        # 参数名称
        for param_name in self.params.keys():
            if param_name not in param_pattern.keys():
                flag = False
        # 参数类型
        for param in param_pattern.items():
            if param[1] == 'N':
                param_name = param[0]
                # 单参数
                if '/' not in list(param_name):
                    if param_name not in self.params.keys() or self.params[param_name] is None:
                        flag = False
                # 多参数
                else:
                    flag = False
                    for single_param_name in param_name.split('/'):
                        if self.params[single_param_name] is not None:
                            flag = True
        if not flag:
            self.function_abbr = None
        return flag

    def get_task_function(self):
        valid_bit = self.is_valid()
        if not valid_bit:
            raise Exception("指令格式错误无法获取对应任务函数指针")
        else:
            return TASK_LIST[self.function_abbr]

    def get_task_args(self):
        valid_bit = self.is_valid()
        if not valid_bit:
            raise Exception("指令格式错误无法获取对应任务参数")
        else:
            param_list = {}
            for key in self.params.keys():
                param_list[PARAM_LIST[key]] = self.params[key]
            return param_list

    def to_task(self):
        function = self.get_task_function()
        args = self.get_task_args()
        return Task(function, args)


# 指令头和任务编号对应关系
INSTRUCTION_PATTERNS = {
    "quit param{}": 'EXIT',
    "q param{}": 'EXIT',
    "checkgrades param{y:N;t:N}": 'CHECK_GRADES',
    "checkcurriculum param{y:N;t:N;g:N;m:N}": 'CHECK_CURRICULUM',
    "checknews param{}": 'CHECK_NEWS',
    "applyforexamonly param{cn/ci:N}": 'APPLY_FOR_EXAM_ONLY',
    "cancelexamonly param{cn/ci:N}": 'CANCEL_EXAM_ONLY'
}
