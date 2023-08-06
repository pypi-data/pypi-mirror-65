import json

import xlwt
from xlwt import Font

from jiaowu.core.function.utils.formatter import ClassInfoFormatter
from jiaowu.core.interface.tools import Writer
from jiaowu.data.constants.status_code import StatusCode as Code


class TBExcelWriter(Writer):
    """
    write timetable as excel
    """

    def write(self, data, file_path):
        info_list = []
        for course_info in data:
            formatter = ClassInfoFormatter(course_info)
            format_data = formatter.format()
            for x in format_data:
                info_list.append(x)
        try:
            li = ['', '一', '二', '三', '四', '五']
            workbook = xlwt.Workbook(encoding='utf-8')
            sheet = workbook.add_sheet("课程表")

            # 单元格文字居中
            style = xlwt.XFStyle
            al = xlwt.Alignment()
            al.horz = 0x02  # 设置水平居中
            al.vert = 0x01  # 设置垂直居中
            style.alignment = al
            fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
            fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
            style.font = fnt
            style.num_format_str = 'yyyy-mm-dd'  # 日期格式
            style.borders = xlwt.Formatting.Borders()
            style.pattern = xlwt.Formatting.Pattern()
            style.protection = xlwt.Formatting.Protection()

            for i in range(6):
                sheet.write(0, i, li[i], style=style)
            for i in range(1, 12):
                sheet.write(i, 0, str(i), style=style)
            flags = [-1] * len(info_list)
            corporated_info_list = []
            for y in range(len(info_list)):
                # 先做一遍遍历，将相同时间段的课程信息合并
                if flags[y] < 0:
                    corporated_info = info_list[y][0]
                    for j in range(y + 1, len(info_list)):
                        if flags[j] < 0 and info_list[j][1] == info_list[y][1] and info_list[j][2] == info_list[y][2]:
                            flags[j] = 0
                            corporated_info += "\n" + info_list[j][0]
                    flags[y] = 0
                    corporated_info_list.append((corporated_info, info_list[y][1], info_list[y][2]))
            for x in corporated_info_list:
                sheet.write_merge(x[2][0], x[2][1], x[1], x[1], x[0], style=style)
            # 设置单元格格式
            for i in range(1, 6):
                col = sheet.col(i)
                col.width = 256 * 35
                col.height = 256 * 25

            workbook.save(file_path)

        except Exception as e:
            print(e)
            print(Code.CANNOT_SAVE_AS_EXCEL.get_msg())


class TBPdfWriter(Writer):
    """
     write timetable as pdf
    """
    def write(self, content, url):
        pass

class JSONWriter(Writer):
    def write(self, content, url):
        assert type(content)==dict
        with open(url,'w',encoding='utf-8') as f:
            json.dump(content,f,ensure_ascii=False)
