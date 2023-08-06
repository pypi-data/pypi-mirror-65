from src.core.function.utils.parser import TLparser


class ClassInfoFormatter:
    def __init__(self, class_info):
        self.class_info = class_info

    def format(self):
        x = []
        class_name = self.class_info.name
        class_tl = self.class_info.time_and_loc
        tl_parser = TLparser()
        class_tl_parse = tl_parser.parse(class_tl)
        for ele in class_tl_parse:
            format_str = class_name + " " + ele[3] + "<" + ele[2] + ">"
            x.append((format_str, ele[0], ele[1]))
        return x
