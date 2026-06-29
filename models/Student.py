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

# class Student_Financial_Info(SQLModel, table=True):  # 账务系统学生信息表
#     __tablename__ = "PXSDM"
#     XH: str = Field(primary_key=True)  # 学号
#     XM: str  # 姓名
#     bmbh: str   # 部门编号 未使用
#     ZJM: str    # 拼音缩写
#     BMDM: str    # 部门代码
#     bmmc: str    # 部门名称
#     XSXZDM: str
#     XSXZMC: str
#     rylx: str
#     mobie: str
#     lxdh: str
#     email: str
#     ickh: str
#     yhzh: str   # 银行账号
#     sfzh: str
#     khhmc: str
#     zhlb: str


class Student_Charging_Info(SQLModel, table=True):  # 收费系统学生信息表
    __tablename__ = "PXSDM"
    XH: str = Field(primary_key=True)  # 学号
    XM: str  # 姓名
    XB: str   # 性别
    ZJM: str  #  助记码
    ISLS: str  # 无效字段
    RXND: str  # 入学年度
    LXND: str  # 离校年度
    BMDM: str  # 部门代码
    ZYDM: str  # 专业代码
    BJDM: str # 班级代码
    XSXZDM: str # 学生性质代码
    XSLYDM: str #  学生来源代码
    CSRQ: str  #   出生日期
    JTZZ: str # 家庭住址
    YYDM: str
    YHZH: str  # 银行账号
    ICKH: str  # IC卡号
    SFZH: str  # 身份证号
    ISOK: str  # 是否启动
    BZ: str  # 备注
    SSDQ: str # 所属地区
    XSZTDM: str # 学生状态代码
    BDYY: str  # 变动原因
    ISFFBZJ: str  # 是否发放补助
    XSSX1: str
    XSSX2: str
    XSSX3: str
    XSSX4: str
    UF_01: str
    UF_02: str
    UF_03: str
    UF_04: str
    UF_05: str
    UF_06: str
    UF_07: str
    UF_08: str
    UF_09: str
    UF_10: str
    XZ: str  # 学制
    XSLBDM: str #  学生类别代码
    XMJC: str  # 姓名简称
    TEL: str  # 手机号
    EMAIL: str  # 电子邮箱
    ZJLBDM: str  #
    KSH: str # 考生号
    MZDM: str # 民族代码
    ISJM: str  # 是否剧名
    dwjgbm: str  # 单位机构代码
    FXDM: str  # 校区代码
    XGRQ: str  # 修改日期
    XGR: str  #修改人
    ssdm: str  # 宿舍代码
    ISSXLW: str  # 是否时许劳务
    SXLWSJ: str  # 实习劳务时间
    JSFA: str  # 计税方案
    zhlb: str # 账号类别
    yh: str # 开户行
    khhmc: str # 开户行名称
    lhh: str  # 联行号


class  Class_Info(SQLModel, table=True):  # 收费系统班级表
    __tablename__ = "PBJDM"
    BJDM: str = Field(primary_key=True)  # 班级代码
    BJMC: str  # 班级名称
    BMDM: str   # 部门代码
    ZYDM: str
    RXND: str
    LXND: str
    QYF: str
    BZ: str
    BJSX1: str
    BJSX2: str
    XZ: str
    fdygh: str
    fdyxm: str
    fdytel: str
    FXDM: str
    XGRQ: str
    XGR: str

class  Department_Info(SQLModel, table=True):  # 收费系统部门表
    __tablename__ = "PBMDM"
    BMDM: str = Field(primary_key=True)  # 部门代码
    BMMC: str # 部门名称
    JC: str
    MX: str
    QYF: str
    MADD: str
    TCODE: str
    BZ: str
    BMSX1: str
    BMSX2: str
    FXDM: str
    XGRQ: str
    XGR: str

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


def get_student_info(student_id: str):
    """
    根据学号获取学生完整信息：姓名、班级名称、部门名称、银行卡号
    :param student_id: 学号
    :return: 字典格式学生信息，无数据返回None
    """
    with Session(student_expense_engine) as session:
        # 多表联查：学生表 + 班级表 + 部门表
        # 1. 学生表关联班级表（BJDM）
        # 2. 学生表关联部门表（BMDM）
        statement = (
            select(
                # 学生基础信息
                Student_Charging_Info.XH,
                Student_Charging_Info.XM,
                Student_Charging_Info.YHZH,
                # 班级名称
                Class_Info.BJMC,
                # 部门名称
                Department_Info.BMMC)
            .join(Class_Info, Student_Charging_Info.BJDM == Class_Info.BJDM, isouter=True)
            .join(Department_Info, Student_Charging_Info.BMDM == Department_Info.BMDM, isouter=True)
            .where(Student_Charging_Info.XH == student_id)
        )

        # 获取单条学生记录
        student = session.exec(statement).first()

        if not student:
            return None

        # 构造返回数据
        return {
            "学号": student.XH,
            "姓名": student.XM,
            "班级名称": student.BJMC or "未分配班级",
            "部门名称": student.BMMC or "未分配部门",
            "银行卡号": student.YHZH or "无银行卡信息"
        }

