import logging
from models.ArrearsStudent import (
    get_arrears_students,
    get_arrears_statistics_by_grade,
    get_arrears_statistics_by_department
)

logger = logging.getLogger(__name__)


def get_arrears_student_details(grade: str, fee_year: str):
    """
    获取指定学生年级、收费年度的欠费学生明细

    :param grade: 学生年级（入学年度，如 "2025"）
    :param fee_year: 收费年度（收费期间代码，如 "2025"）
    :return: 欠费学生明细列表
    """
    try:
        return get_arrears_students(grade, fee_year)
    except Exception as e:
        logger.error(f"获取欠费学生明细失败：{str(e)}", exc_info=True)
        raise


def get_arrears_grade_statistics(fee_year: str):
    """
    按年级统计指定收费年度的欠费学生人数

    :param fee_year: 收费年度（收费期间代码，如 "2025"）
    :return: 按年级统计结果
    """
    try:
        return get_arrears_statistics_by_grade(fee_year)
    except Exception as e:
        logger.error(f"获取年级欠费统计失败：{str(e)}", exc_info=True)
        raise


def get_arrears_department_statistics(fee_year: str):
    """
    按学院统计指定收费年度的欠费学生人数

    :param fee_year: 收费年度（收费期间代码，如 "2025"）
    :return: 按学院统计结果
    """
    try:
        return get_arrears_statistics_by_department(fee_year)
    except Exception as e:
        logger.error(f"获取学院欠费统计失败：{str(e)}", exc_info=True)
        raise


def get_department_arrears_details(grade: str, fee_year: str, department_code: str):
    """
    获取指定学院、学生年级、收费年度的欠费学生明细

    :param grade: 学生年级（入学年度，如 "2025"）
    :param fee_year: 收费年度（收费期间代码，如 "2025"）
    :param department_code: 学院代码
    :return: 欠费学生明细列表
    """
    try:
        return get_arrears_students(grade, fee_year, department_code)
    except Exception as e:
        logger.error(f"获取学院欠费明细失败：{str(e)}", exc_info=True)
        raise
