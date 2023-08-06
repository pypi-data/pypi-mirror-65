import os
import re

import pytesseract as pytesseract
from PIL import Image


# 识别验证码
from src.core.function.utils.writer import JSONWriter
from src.core.model.spider_model import LoginSpider


def recognize_captcha(file_path):
    image = Image.open(file_path)
    print(image.size)
    image = image.crop((1, 1, 70, 19))
    # 灰度化
    gray = image.convert('L')
    # gray.show()
    data = gray.load()
    w, h = image.size
    for i in range(w):
        for j in range(h):
            if data[i, j] > 129:
                data[i, j] = 255
            else:
                data[i, j] = 0
    gray.show()
    result = pytesseract.image_to_string(gray)
    result = ''.join([x for x in list(result) if x != ' '])
    return result

def crawl_speciality_select(spider:LoginSpider):
    #爬取院系对应的编号
    #**273%金融工程((
    #A41%*外国语言文学类((
    reflection_table={}
    spider.update_header("Pragma","no-cache")
    response=spider.task.get(url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getTermAcademy")
    pattern1=re.compile("\*\*(\d\d\d)%([\u4e00-\u9fa5a-zA-Z0-9()]+)\(\(")
    pattern2=re.compile("(\S\S\S)%\*([\u4e00-\u9fa5a-zA-Z0-9()]+)\(\(")
    reflections1=re.findall(pattern1,response.text)
    reflections2=re.findall(pattern2,response.text)
    for reflection in reflections1:
        reflection_table[reflection[1]]=reflection[0]
    for reflection in reflections2:
        reflection_table[reflection[1]]=reflection[0]
    json_writer=JSONWriter()
    curPath=os.path.abspath(os.path.dirname(__file__))
    paths_part=curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath='\\'.join(paths_part)
    print(rootPath)
    json_writer.write(reflection_table,rootPath+"\\data\\output\\reflection.json")
    print("一共有%d个专业"%(len(reflections1)+len(reflections2)))
