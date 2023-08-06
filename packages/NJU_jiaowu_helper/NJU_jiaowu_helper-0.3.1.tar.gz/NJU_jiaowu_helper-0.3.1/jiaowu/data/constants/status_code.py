from enum import Enum, unique


@unique
class StatusCode(Enum):
    COURSE_NOT_FOUND = (1, "该课程不存在")
    APPLICATION_BEYOND_MAX_LIMITS = (2, "已申请的课程数达到上限")
    COURSE_NOT_EXIST_IN_LIST = (3, "课程不在相应的列表中")
    CANNOT_SAVE_AS_EXCEL = (4, "无法转化为excel格式存储")
    PWD_UPDATE_SUCCESS=(5,"密码修改成功")
    PWD_UPDATE_FAILURE = (6, "密码修改失败")

    def get_msg(self):
        return self.value[1]

    def get_code(self):
        return self.value[0]
