import json
import os

from scrapy import Selector

from src.core.function.utils.others import crawl_speciality_select
from src.core.model.data_model import Course
from src.core.model.spider_model import LoginSpider


# 下载信息功能
def check_grades(spider: LoginSpider, year, term):
    # 查看成绩
    course_list = []
    spider.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/studentinfo/index.do")
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList" + "&termCode=" + str(
            year) + str(term))
    grades_table = Selector(text=response.text).xpath("//tr[@class='TABLE_TR_01']") + Selector(
        text=response.text).xpath("//tr[@class='TABLE_TR_02']")
    for selector in grades_table:
        course = Course()
        tds = selector.xpath("./td")
        # print(len(tds))
        course.id = tds[1].xpath("./a/u/text()")[0].extract()
        # print(course.id)
        course.name = tds[2].xpath("./text()")[0].extract()
        # print(course.name)
        course.type = tds[4].xpath("./text()")[0].extract().strip()
        # print(course.type)
        credit = tds[5].xpath("./text()").extract()
        if len(credit) > 0:
            course.credit = credit[0]
        print(course.credit)
        course.mark = tds[6].xpath("./ul/text()")[0].extract().strip()
        # print(course.mark)
        course_list.append(course)

    # print(grades_table)
    return course_list


def get_timetable(spider: LoginSpider):
    # 下载课程表
    spider.update_header("Referer", "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/index.do")
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=currentTermCourse")
    course_table = Selector(text=response.text).xpath("//tr[@class='TABLE_TR_01']") + Selector(
        text=response.text).xpath("//tr[@class='TABLE_TR_02']")
    course_list = []
    for selector in course_table:
        course = Course()
        tds = selector.xpath("./td")
        # print(len(tds))
        course.id = tds[0].xpath("./a/u/text()")[0].extract().strip()
        # print(course.id)
        course.name = tds[1].xpath("./text()")[0].extract().strip()
        # print(course.name)
        course.teacher = tds[3].xpath("./text()")[0].extract().strip()
        # print(course.teacher)
        time_and_loc = tds[4].xpath("./text()")
        str = ""
        for s in time_and_loc:
            str += s.extract().strip() + "\n"
        course.time_and_loc = str
        # print(course.time_and_loc)
        course.type = tds[6].xpath("./text()")[0].extract().strip()
        # print(course.type)
        comments = tds[8].xpath("./b/text()")
        if len(comments) > 0:
            course.comments = comments[0].extract().strip()
        # print(course.comments)
        course_list.append(course)
    return course_list


def crawl_news(spider: LoginSpider, start=0, end=100):
    # 爬取首页通知
    return 0


def check_course_info(spider: LoginSpider, year, term, grade, major):
    #查询院系课程
    spider.update_header("Referer",
                         "http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getTermAcademy")
    curPath = os.path.abspath(os.path.dirname(__file__))
    paths_part = curPath.split('\\')
    for i in range(3):
        paths_part.pop()
    rootPath = '\\'.join(paths_part)
    reflection_json_path = rootPath + "\\data\\output\\reflection.json"
    if not os.path.exists(reflection_json_path):
        crawl_speciality_select(spider)
    fp = open(reflection_json_path, 'r',encoding="utf-8")
    major_index = json.load(fp)[major]
    url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/allCourseList.do?method=getCourseList"+"&curTerm="+str(year)+str(term)+"&curSpeciality="+major_index+"&curGrade="+str(grade)
    response=spider.task.get(url=url)
    selector=Selector(text=response.text)
    course_selectors=selector.xpath("//tr[@class='TABLE_TR_01']")+selector.xpath("//tr[@class='TABLE_TR_02']")
    course_list=[]
    for selector in course_selectors:
        tds=selector.css("td")
        course=Course()
        course.id = tds[0].css("a>u::text")[0].get().strip()
        course.name=tds[1].xpath("./text()").get().strip()
        course.type=tds[2].xpath("./text()").get().strip()
        course.credit=tds[4].xpath("./text()").get().strip()
        course.teacher=tds[7].xpath("./text()").get().strip()
        course.time_and_loc=tds[8].xpath("./text()").get().strip()
        #print(course)
        course_list.append(course)
    return course_list




