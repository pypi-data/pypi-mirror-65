import re

from scrapy import Selector
from jiaowu.data.constants.status_code import StatusCode as Code
from jiaowu.core.model.spider_model import LoginSpider


def apply_for_exam_only(spider: LoginSpider, course_name=None, course_id=None):
    # 申请免修不免靠
    spider.update_header("Referer", 'http://elite.nju.edu.cn/jiaowu/student/elective/index.do')
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKList")
    selector = Selector(text=response.text)
    trs = selector.xpath("//tr[@align='left']")
    class_id = ""
    for tr in trs:
        if tr.xpath("./td/text()")[0].extract() == course_id or tr.xpath("./td/text()")[1].extract() == course_name:
            class_id = re.search(re.compile("\((\d+)\)"),
                                 tr.xpath("./td")[3].xpath("./a/@href")[0].extract()).group(1)
    if len(class_id) > 0:
        # 检测已申请的课程是否在规定数量之内
        if len(selector.xpath("//div[@id='courseList']")[0].css("table tr[align='left']")) >= 2:
            print(Code.APPLICATION_BEYOND_MAX_LIMITS.get_msg())
            return
        spider.task.get(
            url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKApply&classId=%s" % class_id)
    else:
        print(Code.COURSE_NOT_FOUND.get_msg())


def cancel_exam_only_application(spider: LoginSpider, course_name=None, course_id=None):
    # 取消免修不免靠申请
    spider.update_header("Referer", 'http://elite.nju.edu.cn/jiaowu/student/elective/index.do')
    response = spider.task.get(
        url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKList")
    selector = Selector(text=response.text)
    trs = selector.xpath("//tr[@align='left']")
    class_id = ""
    for tr in trs:
        if tr.xpath("./td/text()")[0].extract() == course_id or tr.xpath("./td/text()")[1].extract() == course_name:
            class_id = re.search(re.compile("\((\d+)\)"),
                                 tr.xpath("./td")[3].xpath("./a/@href")[0].extract()).group(1)
    if len(class_id) > 0:
        # 检测是否在待审核列表
        application_list = selector.xpath("//div[@id='courseList']/table")[0].css("tr[align='left']")
        flag = False
        for application in application_list:
            tds_text = application.xpath("./td/text()").extract()
            if tds_text[0] == course_id or tds_text[1] == course_name:
                flag = True
        if not flag:
            print(Code.COURSE_NOT_EXIST_IN_LIST.get_msg())
            return
        spider.task.get(
            url="http://elite.nju.edu.cn/jiaowu/student/teachinginfo/courseList.do?method=exemptionBMKDelete&classId=%s" % class_id)
    else:
        print(Code.COURSE_NOT_FOUND.get_msg())


def update_password(spider: LoginSpider, old_pwd, new_pwd):
    #修改密码
    spider.update_header("Referer",
                         'http://elite.nju.edu.cn/jiaowu/student/basicinfo/ModifyPassword.do?method=editStudentPassword')
    form = {
        'OldPassword': old_pwd,
        'NewPassword': new_pwd,
        'NewPassword_d': new_pwd
    }
    response = spider.task.post(
        url="http://elite.nju.edu.cn/jiaowu/student/basicinfo/ModifyPassword.do?method=editStudentPassword", data=form)
    if len(re.findall("密码修改成功", response.text)) >= 2:
        print(Code.PWD_UPDATE_SUCCESS.get_msg())
    else:
        print(Code.PWD_UPDATE_FAILURE.get_msg())
