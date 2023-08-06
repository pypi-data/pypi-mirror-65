class Course:
    def __init__(self, id=None, name=None, mark=None, type=None, credit=None, teacher=None, time_and_loc=None,
                 comments=None):
        self.id = id
        self.name = name
        self.mark = mark
        self.type = type
        self.credit = credit
        self.teacher = teacher
        self.time_and_loc = time_and_loc
        self.comments = comments
    def __str__(self):
        s="课程信息("
        attributes=[x for x in dir(self) if not x.startswith("__")]
        for attr in attributes:
            if getattr(self,attr) is not None:
                if len(s)>5:
                    s+=";"
                s+=attr+":"+str(getattr(self,attr))
        s+=')'
        return s

if __name__ == '__main__':
    print(Course(id=1,name="软工导学"))
