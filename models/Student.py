from sqlmodel import SQLModel, Field, select, Session, DateTime
from typing import Optional
from db import student_expense_engine
from decimal import Decimal


class Student_Toll(SQLModel, table=True):  # 收费表
    __tablename__ = "SF_ZZ"
    XH: str = Field(primary_key=True)  # 学号

    SFQJDM: str = Field(primary_key=True)

    SFXMDM: str = Field(primary_key=True)  # 收费项目代码

    YJJE: Decimal = Field(default=0, max_digits=18, decimal_places=2)  # 应交金额

    TFJE: Decimal = Field(default=0, max_digits=18, decimal_places=2)  # 退费金额

    JMJE: Decimal = Field(default=0, max_digits=18, decimal_places=2)  # 减免金额

    SJJE: Decimal = Field(default=0, max_digits=18, decimal_places=2)  # 实缴金额

    FIELD1: Decimal = Field(default=0, max_digits=18, decimal_places=2)

    FIELD2: Decimal = Field(default=0, max_digits=18, decimal_places=2)

    ISDY: bool

    XGR: str

    FXDM: str

    xgrq: str


# class Student_Accounts_Receivablee(SQLModel, table=True):  # 应收款表
#     __tablename__ = "SF_YSK"
#     XH: str = Field(primary_key=True)  # 学号
#     SFQJDM: str = Field(primary_key=True)
#
#     SFXMDM: str = Field(primary_key=True)  # 收费项目代码
#
#     YSJE: Decimal = Field(default=0, max_digits=18, decimal_places=2)  # 应收金额
#
#     HZR: str
#     ISHZ: bool
#     SCR: str
#     SCRQ: str
#     FSBZBM: str
#     FSSFXM: str
#     XGR: str
#     XGRQ: str
#     FXDM: str

#
# def get_student_accounts_receivablee(student_id: str):
#     """
#     获取学生应收款
#     :param student_id:
#     :return:
#     """
#     with Session(student_expense_engine) as session:
#         statement = select(Student_Accounts_Receivablee).where(Student_Accounts_Receivablee.XH == student_id)
#         results = session.exec(statement).all()
#         if results:
#             return results
#

def get_student_toll(student_id: str):
    """
    获取学生缴费信息
    :param student_id:
    :return:
    """
    with Session(student_expense_engine) as session:
        statement = select(Student_Toll).where(Student_Toll.XH == student_id)
        results = session.exec(statement).all()
        if results:
            return results
