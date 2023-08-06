from jiaowu.core.function.download.download_functions import check_grades, get_timetable, crawl_news
from jiaowu.core.function.exit.exit import terminate
from jiaowu.core.function.upload.upload_functions import apply_for_exam_only, cancel_exam_only_application

# 任务编号和对应的函数指针
TASK_LIST={
    # DOWNLOAD
    "CHECK_GRADES" :check_grades,
    "CHECK_CURRICULUM" : get_timetable,
    "CHECK_NEWS" : crawl_news,
    # UPLOAD
    "APPLY_FOR_EXAM_ONLY" : apply_for_exam_only,
    "CANCEL_EXAM_ONLY" :cancel_exam_only_application,
    "EXIT":terminate
}

#参数简写及对应的参数名
PARAM_LIST={
    'y':"year",
    't':"term",
    'g':'grade',
    'm':'major',
    'op':'old_pwd',
    'np':'new_pwd',
    'cn':'course_name',
    'ci':'course_id'


}
