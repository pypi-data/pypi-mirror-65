import re

from jiaowu.core.interface.tools import Parser


class TLparser(Parser):
    """
    Time and Loc Parser
    """

    def parse(self, data):
        reflection = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7}
        pattern = re.compile("周([一二三四五六日]) 第(\d+)-(\d+)节 (\S+.*周) (.+)\n*")
        result = re.findall(pattern, data)
        all_arrangement = []
        if len(result) > 0:
            for sub_result in result:
                # 天
                day = reflection[sub_result[0]]
                # 时间段
                lesson = (int(sub_result[1]), int(sub_result[2]))
                # 周
                x = sub_result[3]
                week = ""
                if re.match("(\d+-\d+)周", x):
                    week = re.match("(\d+-\d+)周", x).group(1)
                elif x == '单周':
                    week = '单'
                elif x == '双周':
                    week = '双'
                else:
                    y = re.findall(re.compile("第(\d+)周"), x)
                    weeks = []
                    for z in y:
                        weeks.append(z)
                    week = ','.join(weeks)

                # 地点
                loc = sub_result[4].strip()
                all_arrangement.append((day, lesson, week, loc))
        return all_arrangement
