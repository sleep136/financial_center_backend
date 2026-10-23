from sqlmodel import SQLModel, select, Session, func
from typing import List, Optional
from db import student_expense_engine
from decimal import Decimal

# 收费系统的基础表模型统一在 models.Student 中定义，
# 此处直接复用，避免同一 MetaData 下重复注册表名（SF_ZZ/PXSDM/PBJDM/PBMDM）
from models.Student import Student_Toll, Student_Charging_Info, Class_Info, Department_Info


class ArrearsStudentDetail(SQLModel):
    """欠费学生明细"""
    xh: str  # 学号
    xm: str  # 姓名
    rxnd: str  # 入学年度（学生年级）
    bmdm: str  # 部门代码
    bmmc: str  # 部门名称
    bjmc: str  # 班级名称
    xsxzdm: str  # 学生性质代码（仅返回展示，不作为过滤条件）
    xsztdm: str  # 学生状态代码（仅返回展示，不作为过滤条件）
    yjje: Decimal  # 应交金额
    sjje: Decimal  # 实缴金额
    qfje: Decimal  # 欠费金额


class ArrearsStatisticsByGrade(SQLModel):
    """按年级统计欠费"""
    rxnd: str  # 入学年度（年级）
    student_count: int  # 欠费学生人数


class ArrearsStatisticsByDepartment(SQLModel):
    """按学院统计欠费"""
    bmdm: str  # 部门代码
    bmmc: str  # 部门名称
    student_count: int  # 欠费学生人数


def get_arrears_students(grade: Optional[str] = None, fee_year: Optional[str] = None,
                         department_code: Optional[str] = None) -> List[ArrearsStudentDetail]:
    """
    获取欠费学生明细

    学生年级取 PXSDM.RXND，收费年度取 SF_ZZ.SFQJDM，两者是相互独立的维度：
    同一收费年度下的欠费学生可能来自多个年级。

    :param grade: 学生年级（入学年度，如 "2025"），None 表示不过滤年级
    :param fee_year: 收费年度（收费期间代码，如 "2025"），None 表示不过滤收费年度
    :param department_code: 学院代码，传入时只返回该学院的欠费学生
    :return: 欠费学生明细列表
    """
    with Session(student_expense_engine) as session:
        conditions = [
            Student_Toll.SFXMDM.in_(['01', '02']),  # 收费项目：01=学费，02=住宿费（默认过滤）
        ]
        if grade:
            conditions.append(Student_Charging_Info.RXND == grade)
        if fee_year:
            conditions.append(Student_Toll.SFQJDM == fee_year)
        if department_code:
            conditions.append(Student_Charging_Info.BMDM == department_code)

        statement = (
            select(
                Student_Charging_Info.XH,
                Student_Charging_Info.XM,
                Student_Charging_Info.RXND,
                Student_Charging_Info.BMDM,
                Department_Info.BMMC,
                Class_Info.BJMC,
                Student_Charging_Info.XSXZDM,
                Student_Charging_Info.XSZTDM,
                func.sum(Student_Toll.YJJE).label('yjje'),
                func.sum(Student_Toll.SJJE).label('sjje'),
                (func.sum(Student_Toll.YJJE) - func.sum(Student_Toll.SJJE)).label('qfje')
            )
            .join(Student_Toll, Student_Charging_Info.XH == Student_Toll.XH)
            .join(Department_Info, Student_Charging_Info.BMDM == Department_Info.BMDM, isouter=True)
            .join(Class_Info, Student_Charging_Info.BJDM == Class_Info.BJDM, isouter=True)
            .where(*conditions)
            .group_by(
                Student_Charging_Info.XH,
                Student_Charging_Info.XM,
                Student_Charging_Info.RXND,
                Student_Charging_Info.BMDM,
                Department_Info.BMMC,
                Class_Info.BJMC,
                Student_Charging_Info.XSXZDM,
                Student_Charging_Info.XSZTDM
            )
            .having((func.sum(Student_Toll.YJJE) - func.sum(Student_Toll.SJJE)) > 0)  # 欠费金额 > 0
            .order_by(Student_Charging_Info.BMDM, Student_Charging_Info.XH)
        )

        results = session.exec(statement).all()

        arrears_list = []
        for row in results:
            arrears_list.append(ArrearsStudentDetail(
                xh=row.XH,
                xm=row.XM,
                rxnd=row.RXND,
                bmdm=row.BMDM,
                bmmc=row.BMMC or "未分配学院",
                bjmc=row.BJMC or "未分配班级",
                xsxzdm=row.XSXZDM,
                xsztdm=row.XSZTDM,
                yjje=row.yjje or 0,
                sjje=row.sjje or 0,
                qfje=row.qfje or 0
            ))

        return arrears_list


def _arrears_students_subquery(fee_year: Optional[str] = None):
    """
    构建"欠费学生"子查询：先按学号聚合出每个学生在指定收费年度的应交/实缴，再筛出欠费的学生。

    SQL Server 不允许聚合函数嵌套聚合函数（sum(sum(...)) 会报错 130），
    因此必须先在内层按学号分组算出欠费金额，外层再按年级/学院统计人数。

    :param fee_year: 收费年度（SF_ZZ.SFQJDM），None 表示不过滤收费年度
    """
    where_conditions = [
        Student_Toll.SFXMDM.in_(['01', '02']),  # 收费项目：01=学费，02=住宿费（默认过滤）
    ]
    if fee_year:
        where_conditions.append(Student_Toll.SFQJDM == fee_year)

    return (
        select(
            Student_Charging_Info.XH,
            Student_Charging_Info.RXND,
            Student_Charging_Info.BMDM
        )
        .join(Student_Toll, Student_Charging_Info.XH == Student_Toll.XH)
        .where(*where_conditions)
        .group_by(
            Student_Charging_Info.XH,
            Student_Charging_Info.RXND,
            Student_Charging_Info.BMDM
        )
        .having((func.sum(Student_Toll.YJJE) - func.sum(Student_Toll.SJJE)) > 0)  # 欠费金额 > 0
        .subquery()
    )


def get_arrears_statistics_by_grade(fee_year: Optional[str] = None) -> List[ArrearsStatisticsByGrade]:
    """
    按年级统计指定收费年度的欠费学生人数

    :param fee_year: 收费年度（SF_ZZ.SFQJDM，如 "2025"），None 表示统计所有收费年度
    :return: 按年级统计结果
    """
    with Session(student_expense_engine) as session:
        arrears_students = _arrears_students_subquery(fee_year)

        statement = (
            select(
                arrears_students.c.RXND,
                func.count().label('student_count')
            )
            .select_from(arrears_students)
            .group_by(arrears_students.c.RXND)
            .order_by(arrears_students.c.RXND)
        )

        results = session.exec(statement).all()

        statistics_list = []
        for row in results:
            statistics_list.append(ArrearsStatisticsByGrade(
                rxnd=row.RXND,
                student_count=row.student_count or 0
            ))

        return statistics_list


def get_arrears_statistics_by_department(fee_year: Optional[str] = None) -> List[ArrearsStatisticsByDepartment]:
    """
    按学院统计指定收费年度的欠费学生人数

    :param fee_year: 收费年度（SF_ZZ.SFQJDM，如 "2025"），None 表示统计所有收费年度
    :return: 按学院统计结果
    """
    with Session(student_expense_engine) as session:
        arrears_students = _arrears_students_subquery(fee_year)

        statement = (
            select(
                arrears_students.c.BMDM,
                Department_Info.BMMC,
                func.count().label('student_count')
            )
            .select_from(arrears_students)
            .join(Department_Info, arrears_students.c.BMDM == Department_Info.BMDM, isouter=True)
            .group_by(
                arrears_students.c.BMDM,
                Department_Info.BMMC
            )
            .order_by(func.count().desc())
        )

        results = session.exec(statement).all()

        statistics_list = []
        for row in results:
            statistics_list.append(ArrearsStatisticsByDepartment(
                bmdm=row.BMDM,
                bmmc=row.BMMC or "未分配学院",
                student_count=row.student_count or 0
            ))

        return statistics_list
