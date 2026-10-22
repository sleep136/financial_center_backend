from fastapi import APIRouter, HTTPException, status
from service.arrears_student import (
    get_arrears_student_details,
    get_arrears_grade_statistics,
    get_arrears_department_statistics,
    get_department_arrears_details
)

router = APIRouter()


@router.get("/arrears-students/details/{grade}/{fee_year}")
async def get_arrears_details(grade: str, fee_year: str):
    """
    获取欠费学生明细

    :param grade: 学生年级（入学年度 PXSDM.RXND，如 "2025"）
    :param fee_year: 收费年度（收费期间代码 SF_ZZ.SFQJDM，如 "2025"）
    :return: 欠费学生明细列表
    """
    try:
        details = get_arrears_student_details(grade, fee_year)

        return {
            "grade": grade,
            "fee_year": fee_year,
            "total_count": len(details),
            "students": details
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/arrears-students/statistics/grade/{fee_year}")
async def get_grade_statistics(fee_year: str):
    """
    按年级统计欠费学生人数

    :param fee_year: 收费年度（收费期间代码 SF_ZZ.SFQJDM，如 "2025"）
    :return: 按年级统计结果
    """
    try:
        statistics = get_arrears_grade_statistics(fee_year)

        return {
            "fee_year": fee_year,
            "statistics": statistics
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/arrears-students/statistics/department/{fee_year}")
async def get_department_statistics(fee_year: str):
    """
    按学院统计欠费学生人数

    :param fee_year: 收费年度（收费期间代码 SF_ZZ.SFQJDM，如 "2025"）
    :return: 按学院统计结果
    """
    try:
        statistics = get_arrears_department_statistics(fee_year)

        return {
            "fee_year": fee_year,
            "statistics": statistics
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/arrears-students/department/{grade}/{fee_year}/{department_code}")
async def get_department_details(grade: str, fee_year: str, department_code: str):
    """
    获取指定学院的欠费学生明细

    :param grade: 学生年级（入学年度 PXSDM.RXND，如 "2025"）
    :param fee_year: 收费年度（收费期间代码 SF_ZZ.SFQJDM，如 "2025"）
    :param department_code: 学院代码
    :return: 欠费学生明细列表
    """
    try:
        details = get_department_arrears_details(grade, fee_year, department_code)

        return {
            "grade": grade,
            "fee_year": fee_year,
            "department_code": department_code,
            "total_count": len(details),
            "students": details
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )
