# 任务和对应的函数指针
from enum import Enum
from src.core.function.download.download_functions import check_grades, get_timetable, crawl_news
from src.core.function.upload.upload_functions import apply_for_exam_only, cancel_exam_only_application


class TASKNAME(Enum):
    # DOWNLOAD
    CHECK_GRADES = check_grades
    CHECK_CURRICULUM = get_timetable
    CHECK_NEWS = crawl_news
    # UPLOAD
    APPLY_FOR_EXAM_ONLY = apply_for_exam_only
    CANCEL_EXAM_ONLY = cancel_exam_only_application
