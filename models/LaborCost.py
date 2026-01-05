from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import reimbursement_engine


# 劳务相关

class OnCampusPersonnelLaborCost(SQLModel, table=True):
    """
    校内劳务
    """
    __tablename__ = "GSSB_GXSFFB"
    __table_args__ = {'schema': "wssbnew"}
    NIAN: str = Field(default=None)  # 年
    YUE: str = Field(default=None)  # 月
    LSH: str = Field(default=None, primary_key=True)  # 序列号
    RYDM: str = Field(default=None)  # 人员代码
    RYMC: str = Field(default=None)  # 人员姓名
    YHZH: str = Field(default=None, )  # 人员账号
    DWMC: str = Field(default=None)  # 单位名称
    FFXMDM: str = Field(default=None)  # 分系统代码
    KMBH: str = Field(default=None)  # 班级代码
    ZY: str = Field(default=None)  # 专业代码
    JE: str = Field(default=None)  # 金额
    BCKS: str = Field(default=None)  # 班级名称
    SL: str = Field(default=None)  # 人数
    SFJE: str = Field(default=None)  # 是否金额
    STATE: str = Field(default=None)  # 状态
    SHR: str = Field(default=None)  # 审核人
    BZ: str = Field(default=None)  # 备注
    CZY: str = Field(default=None)  # 操作人
    LRRQ: str = Field(default=None)  # 录入日期
    SFZH: str = Field(default=None)  # 身份证号
    ERRMSG: str = Field(default=None)  # 错误信息
    FFLBDM: str = Field(default=None)
    ITEM01: str = Field(default=None)  # 项目01
    ITEM02: str = Field(default=None)  # 项目02
    ITEM03: str = Field(default=None)  # 项目03
    ITEM04: str = Field(default=None)  # 项目04
    ITEM05: str = Field(default=None)  # 项目05
    JE01: str = Field(default=None)  # 金额01
    JE02: str = Field(default=None)  # 金额02
    JE03: str = Field(default=None)  # 金额03
    JE04: str = Field(default=None)  # 金额04
    JE05: str = Field(default=None)  # 金额05
    XMLBDM: str = Field(default=None)  # 项目类别代码
    SFZHT: str = Field(default=None)  #
    YHZHT: str = Field(default=None)  #
    BMBH: str = Field(default=None)  # 班级代码
    XMBH: str = Field(default=None)  # 项目代码
    XMNM: str = Field(default=None)  # 项目名称
    JBR: str = Field(default=None)  # 经办人
    FFFS: str = Field(default=None)  # 付款方式
    BXKM: str = Field(default=None)  # 报销项目
    JJFLKMBH: str = Field(default=None)
    XUHAO: str = Field(default=None)  # 序号
    PZNM: str = Field(default=None)  # 凭证名称
    ISPZ: str = Field(default=None)  # 是否凭证
    ITEM06: str = Field(default=None)  # 项目06
    ITEM07: str = Field(default=None)  # 项目07
    ITEM08: str = Field(default=None)  # 项目08
    ITEM09: str = Field(default=None)  # 项目09
    ITEM10: str = Field(default=None)  # 项目10
    EDKZBM: str = Field(default=None)  # 项目类别代码
    UPRICE: str = Field(default=None)  # 单价
    QUANTITY: str = Field(default=None)  # 数量
    ZYS: str = Field(default=None)  # 专业代码
    CONTENT: str = Field(default=None)  # 项目名称
    QSNY: str = Field(default=None)  # 起算年月
    ZZNY: str = Field(default=None)  # 止算年月
    ITEM11: str = Field(default=None)  # 项目11
    ITEM12: str = Field(default=None)  # 项目12
    ITEM13: str = Field(default=None)  # 项目13
    ITEM14: str = Field(default=None)  # 项目14
    ITEM15: str = Field(default=None)  # 项目15
    ITEM16: str = Field(default=None)  # 项目16
    ITEM17: str = Field(default=None)  # 项目17
    ITEM18: str = Field(default=None)  # 项目18
    ITEM19: str = Field(default=None)  # 项目19
    ITEM20: str = Field(default=None)  # 项目20
    CUSTOM: str = Field(default=None)  # 自定义项目
    ITEM21: str = Field(default=None)  # 项目21
    ITEM22: str = Field(default=None)  # 项目22
    ITEM23: str = Field(default=None)  # 项目23
    ITEM24: str = Field(default=None)  # 项目24
    ITEM25: str = Field(default=None)  # 项目25
    ITEM26: str = Field(default=None)  # 项目26
    ITEM27: str = Field(default=None)  # 项目27
    ITEM28: str = Field(default=None)  # 项目28
    ITEM29: str = Field(default=None)  # 项目29
    ITEM30: str = Field(default=None)  # 项目30
    DCH: str = Field(default=None)
    SCHOOLAREA: str = Field(default=None)  # 学校区域
    ZCMC: str = Field(default=None)  # 专业名称
    ZT: str = Field(default=None)  # 状态
    WTIME: str = Field(default=None)  # 操作时间
    CONSULT: str = Field(default=None)  # 咨询人
    TELNO: str = Field(default=None)  # 联系电话
    BYS: str = Field(default=None)
    DWSTR: str = Field(default=None)
    KHHSTR: str = Field(default=None)
    ISTAMP: str = Field(default=None)
    YHZHN: str = Field(default=None)
    FFMS: str = Field(default=None)


class OffCampusPersonnelLaborCost(SQLModel, table=True):
    """
    校外劳务
    """
    __tablename__ = "GSSB_WLWSFFB"
    __table_args__ = {'schema': "wssbnew"}
    NIAN: str = Field(default=None)  # 年
    YUE: str = Field(default=None)  # 月
    LSH: str = Field(default=None, primary_key=True)  # 序列编号
    RYDM: str = Field(default=None)  # 人员代码
    RYMC: str = Field(default=None)  # 人员名称
    YHZH: str = Field(default=None)  # 银行账号
    FFXMDM: str = Field(default=None)  # 付款方式代码
    KMBH: str = Field(default=None)  # 班级代码
    ZY: str = Field(default=None)  # 专业代码
    JE: str = Field(default=None)  # 金额
    BCKS: str = Field(default=None)  # 班级名称
    SL: str = Field(default=None)  # 数量
    SFJE: str = Field(default=None)  # 是否金额
    STATE: str = Field(default=None)  # 状态
    SHR: str = Field(default=None)  # 审核人
    BZ: str = Field(default=None)  # 备注
    CZY: str = Field(default=None)  # 操作人
    LRRQ: str = Field(default=None)  # 录入日期
    SFZH: str = Field(default=None)  # 是否有效
    ERRMSG: str = Field(default=None)  # 错误信息
    ZJLX: str = Field(default=None)  # 证件类型
    XUHAO: str = Field(default=None)  # 序号
    ITEM01: str = Field(default=None)  # 项目01
    ITEM02: str = Field(default=None)  # 项目02
    ITEM03: str = Field(default=None)  # 项目03
    ITEM04: str = Field(default=None)  # 项目04
    ITEM05: str = Field(default=None)  # 项目05
    JE01: str = Field(default=None)  # 金额01
    JE02: str = Field(default=None)  # 金额02
    JE03: str = Field(default=None)  # 金额03
    JE04: str = Field(default=None)  # 金额04
    JE05: str = Field(default=None)  # 金额05
    KBANK: str = Field(default=None)  # 开户行
    KHYH: str = Field(default=None)  # 开户行账号
    LHH: str = Field(default=None)  # 联系电话
    DFDQ: str = Field(default=None)  # 地址
    XMLBDM: str = Field(default=None)  # 项目类别代码
    BMBH: str = Field(default=None)  # 班级代码
    XMBH: str = Field(default=None)  # 项目代码
    XMNM: str = Field(default=None)  # 项目名称
    YHZHT: str = Field(default=None)  # 银行账号
    JBR: str = Field(default=None)  # 经办人
    FFFS: str = Field(default=None)  # 付款方式
    XWKM: str = Field(default=None)  # 现金账户
    JJFLKMBH: str = Field(default=None)  # 结算班级代码
    PZNM: str = Field(default=None)  # 项目名称
    ISPZ: str = Field(default=None)  # 是否项目
    ITEM06: str = Field(default=None)  # 项目06
    ITEM07: str = Field(default=None)  # 项目07
    ITEM08: str = Field(default=None)  # 项目08
    ITEM09: str = Field(default=None)  # 项目09
    ITEM10: str = Field(default=None)  # 项目10
    EDKZBM: str = Field(default=None)  # 项目类别代码
    UPRICE: str = Field(default=None)  # 单价
    QUANTITY: str = Field(default=None)  # 数量
    ZYS: str = Field(default=None)  # 专业代码
    CONTENT: str = Field(default=None)  # 项目内容
    ITEM11: str = Field(default=None)  # 项目11
    ITEM12: str = Field(default=None)  # 项目12
    ITEM13: str = Field(default=None)  # 项目13
    ITEM14: str = Field(default=None)  # 项目14
    ITEM15: str = Field(default=None)  # 项目15
    ITEM16: str = Field(default=None)  # 项目16
    ITEM17: str = Field(default=None)  # 项目17
    ITEM18: str = Field(default=None)  # 项目18
    ITEM19: str = Field(default=None)  # 项目19
    ITEM20: str = Field(default=None)  # 项目20
    CUSTOM: str = Field(default=None)  # 自定义项目
    ITEM21: str = Field(default=None)  # 项目21
    ITEM22: str = Field(default=None)  # 项目22
    ITEM23: str = Field(default=None)  # 项目23
    ITEM24: str = Field(default=None)  # 项目24
    ITEM25: str = Field(default=None)  # 项目25
    ITEM26: str = Field(default=None)  # 项目26
    ITEM27: str = Field(default=None)  # 项目27
    ITEM28: str = Field(default=None)  # 项目28
    ITEM29: str = Field(default=None)  # 项目29
    ITEM30: str = Field(default=None)  # 项目30
    DCH: str = Field(default=None)  # 班级名称
    SCHOOLAREA: str = Field(default=None)  # 学校区域
    ZCMC: str = Field(default=None)  # 专业名称
    ZT: str = Field(default=None)  # 状态
    WTIME: str = Field(default=None)  # 工作时间
    CONSULT: str = Field(default=None)  # 咨询人
    TELNO: str = Field(default=None)  # 联系电话
    BYS: str = Field(default=None)
    DWSTR: str = Field(default=None)
    KHHSTR: str = Field(default=None)
    ISTAMP: str = Field(default=None)


class StudentLaborCost(SQLModel, table=True):
    """
    学生劳务
    """
    __tablename__ = "XS_ZYFFB"
    __table_args__ = {'schema': "wssbnew"}
    NIAN: str = Field(default=None)  # 年
    YUE: str = Field(default=None)  # 月
    LSH: str = Field(default=None, primary_key=True)  # 序列编号
    XH: str = Field(default=None)  # 学号
    XM: str = Field(default=None)  # 姓名
    YHZH: str = Field(default=None)  # 银行账号
    FFXMDM: str = Field(default=None)  # 付款方式
    KMBH: str = Field(default=None)  # 班级代码
    ZY: str = Field(default=None)  # 专业代码
    JE: str = Field(default=None)  # 金额
    ISJS: str = Field(default=None)  # 是否劳务
    BZ: str = Field(default=None)  # 备注
    CZY: str = Field(default=None)  # 操作人
    LRRQ: str = Field(default=None)  # 录入日期
    QSNY: str = Field(default=None)  # 起算年
    ZZNY: str = Field(default=None)  # 结束年
    STATE: str = Field(default=None)  # 状态
    SFZH: str = Field(default=None)  # 是否学生
    ERRMSG: str = Field(default=None)  # 错误信息
    LJJS: str = Field(default=None)  # 累计劳务金额
    JSFA: str = Field(default=None)  # 劳务方式
    XUHAO: str = Field(default=None)  # 序号
    ITEM01: str = Field(default=None)  # 项目01
    ITEM02: str = Field(default=None)  # 项目02
    ITEM03: str = Field(default=None)  # 项目03
    ITEM04: str = Field(default=None)  # 项目04
    ITEM05: str = Field(default=None)  # 项目05
    JE01: str = Field(default=None)  # 项目01金额
    JE02: str = Field(default=None)  # 项目02金额
    JE03: str = Field(default=None)  # 项目03金额
    JE04: str = Field(default=None)  # 项目04金额
    JE05: str = Field(default=None)  # 项目05金额
    YHZHT: str = Field(default=None)  # 员工合同号
    SFZHT: str = Field(default=None)  # 学生合同号
    XMLBDM: str = Field(default=None)  # 项目类别代码
    BMBH: str = Field(default=None)  # 班级代码
    XMBH: str = Field(default=None)  # 项目代码
    XMNM: str = Field(default=None)  # 项目名称
    JBR: str = Field(default=None)  # 经办人
    FFFS: str = Field(default=None)  # 付款方式
    ZYFKM: str = Field(default=None)  # 专业费用科目
    JJFLKMBH: str = Field(default=None)  # 经济分类班级代码
    PZNM: str = Field(default=None)  # 项目名称
    ISPZ: str = Field(default=None)  # 是否项目
    ITEM06: str = Field(default=None)  # 项目06
    ITEM07: str = Field(default=None)  # 项目07
    ITEM08: str = Field(default=None)  # 项目08
    ITEM09: str = Field(default=None)  # 项目09
    ITEM10: str = Field(default=None)  # 项目10
    EDKZBM: str = Field(default=None)  # 经济分类项目代码
    ITEM11: str = Field(default=None)  # 项目11
    ITEM12: str = Field(default=None)  # 项目12
    ITEM13: str = Field(default=None)  # 项目13
    ITEM14: str = Field(default=None)  # 项目14
    ITEM15: str = Field(default=None)  # 项目15
    UPRICE: str = Field(default=None)  # 单价
    QUANTITY: str = Field(default=None)  # 数量
    ZYS: str = Field(default=None)  # 专业
    CONTENT: str = Field(default=None)  # 内容
    ITEM16: str = Field(default=None)  # 项目16
    ITEM17: str = Field(default=None)  # 项目17
    ITEM18: str = Field(default=None)  # 项目18
    ITEM19: str = Field(default=None)  # 项目19
    ITEM20: str = Field(default=None)  # 项目20
    SL: str = Field(default=None)  # 数量
    YHZHR: str = Field(default=None)  # 员工合同号
    CUSTOM: str = Field(default=None)  # 客户
    ITEM21: str = Field(default=None)  # 项目21
    ITEM22: str = Field(default=None)  # 项目22
    ITEM23: str = Field(default=None)  # 项目23
    ITEM24: str = Field(default=None)  # 项目24
    ITEM25: str = Field(default=None)  # 项目25
    ITEM26: str = Field(default=None)  # 项目26
    ITEM27: str = Field(default=None)  # 项目27
    ITEM28: str = Field(default=None)  # 项目28
    ITEM29: str = Field(default=None)  # 项目29
    ITEM30: str = Field(default=None)  # 项目30
    DCH: str = Field(default=None)  # 项目31
    SCHOOLAREA: str = Field(default=None)  # 项目32
    ZCMC: str = Field(default=None)  # 项目33
    ZT: str = Field(default=None)  # 状态

    WTIME: str = Field(default=None)  # 项目34
    CONSULT: str = Field(default=None)  # 咨询人
    TELNO: str = Field(default=None)  # 联系电话
    BYS: str = Field(default=None)
    DWSTR: str = Field(default=None)
    KHHSTR: str = Field(default=None)
    ISTAMP: str = Field(default=None)


def get_labor_cost_by_program_id(department_id: int, program_id: int, is_all: bool = False):
    """
    根据项目ID获取劳务详情
    :param department_id: 部门ID
    :param program_id: 项目ID
    :return: 劳务详情
    """
    department_id = int(department_id)
    program_id = int(program_id)
    with Session(reimbursement_engine) as session:
        on_campus_statement = select(OnCampusPersonnelLaborCost).where(
            OnCampusPersonnelLaborCost.BMBH == department_id, OnCampusPersonnelLaborCost.XMBH == program_id)
        if not is_all:
            on_campus_statement = on_campus_statement.where(OnCampusPersonnelLaborCost.STATE != 5)
        result = session.execute(on_campus_statement)
        on_campus_results = result.scalars().all()  # 获取所有结果

        off_campus_statement = select(OffCampusPersonnelLaborCost).where(
            OffCampusPersonnelLaborCost.BMBH == department_id, OffCampusPersonnelLaborCost.XMBH == program_id)
        if not is_all:
            off_campus_statement = off_campus_statement.where(OffCampusPersonnelLaborCost.STATE != 5)

        result = session.execute(off_campus_statement)
        off_campus_results = result.scalars().all()

        student_cost_statement = select(StudentLaborCost).where(
            StudentLaborCost.BMBH == department_id, StudentLaborCost.XMBH == program_id)
        if not is_all:
            student_cost_statement = student_cost_statement.where(StudentLaborCost.STATE != 5)
        result = session.execute(student_cost_statement)
        student_cost_results = result.scalars().all()

        return on_campus_results, off_campus_results, student_cost_results
