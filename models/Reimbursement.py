from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import reimbursement_engine


class Reimbursement(SQLModel, table=True):
    __tablename__ = "YY_PZFL"
    __table_args__ = {'schema': "dgyy"}
    GTBH: str
    YYDH: str = Field(default=None, primary_key=True)  # 预约单号
    YWBH: str = Field(default=None, primary_key=True)  # 业务编号
    BH: int = Field(default=None, primary_key=True)  # ?
    FJZS: int
    KMBH: str  # 项目子项编号
    JJFLKMBH: str  # 经济分类科目编号
    GNKMBH: str
    BMBH: int  # 部门编号
    XMBH: int  # 项目编号
    JJE: float  # ？
    DJE: float  # ？
    ZY: str  # 摘要
    WBBH: str
    HL: str
    JSDH: str
    YWRQ: str
    JWB: str
    DWB: str
    DCH: str
    ZRR: str  # 项目负责人
    ZCLB: str
    ZCBH: str
    GKYSLXDM: str
    GKLKXDM: str
    GKZCLXDM: str
    GKFZDM: str
    XJYHCN: str
    GKJJFLDM: str
    XJLLXM: str
    GKXXM: str
    ISGK: str
    JBR: str  # 经办人
    EDKZBM: str
    DWBH: str
    HTBH: str
    PJH: str
    SRBH: str
    GKYSSXDM: str
    YSKMBH: str
    ISZFK: str  # 是否暂付款
    ISZCK: str  #
    ISXJ: str  #
    ISYH: str  # 是否银行转账
    KTXX: str
    ISZDZX: str
    BKND: str
    ISJJFL: str
    ZFFS: str
    DFDW: str  # 对方工号
    DFCITY: str
    DFYH: str
    DFPRO: str
    DFZH: str
    ZT: int  # 状态 3 已处理 其它为未处理
    ISPZ: str
    CZRQ: str
    CZY: str
    KJND: str
    KJQJ: str
    PZLX: str
    PZBH: str
    SM: str
    FY: str
    FIELD1: str
    FIELD2: str
    FIELD3: str
    FIELD4: str
    FIELD5: str
    FIELD6: str
    FIELD7: str
    FIELD8: str
    FIELD9: str
    FIELD10: str
    ZRRMC: str
    RYLX: str
    JSFS: str
    XMNM: str
    PZNM: str
    SJBXJE: str
    WLRQ: str
    CWSHR: str
    KSSH: str
    YWCCLASS: str
    ZCYWDH: str
    # DJLY: str
    # FPNR: str
    # FIELD11: str
    # FIELD12: str
    # FIELD13: str
    # FIELD14: str
    # FIELD15: str
    # FIELD16: str
    # FIELD17: str
    # FIELD18: str
    # FIELD19: str
    # FIELD20: str
    # FIELD21: str
    # FIELD22: str
    # FIELD23: str
    # FIELD24: str
    # FIELD25: str
    # DJ: str
    # SL: str
    # EJXMBH: str
    # CGLX: str
    # HTZXJHBH: str
    # XTLX: str
    # CZSJ: str
    # BHYJ: str
    # CZR: str
    # JFLB: str
    # JFLBMX: str


class Reimbursement_BX(SQLModel, table=True):
    __tablename__ = "YY_YBBX"
    YWRQ: str  # Y业务日期
    NIAN: str  # 年
    YUE: str  # 月
    YWBH: str = Field(default=None, primary_key=True)  # 业务编号
    BH: int  # ?
    DCPJH: str  #
    YWLX: str  # 业务类型
    BXLXBH: str  # 报销类型编号
    ISXJ: str  # 是否线下
    ISGK: str  # 是否？
    YHZH: str  # 银行账号
    ZHYH: str
    ZHLX: str
    PJLX: str  # 票据类型
    ZY: str  # 摘要
    JJE: float  # ？
    DJE: float  # ？
    DFDW: str  # 对方工号
    DFYH: str  # 对方银行账号
    DFZH: str  # 对方账号
    DFPRO: str
    DFCITY: str
    XM: str  # 对方姓名
    BMBH: str  # 部门编号
    XMBH: str  # 项目编号
    KMBH: str  # 项目子项编号
    ZT: str  # 状态
    JSBH: str  # ？
    JDJEFX: str  # ？
    YYSJ: str  #
    FJZS: str  # ？
    YJSHRFZRBH: str
    YJSHRXM: str
    EJSHRFZRBH: str
    EJSHRXM: str
    SJSHRFZRBH: str
    SJSHRXM: str
    FZRBH: str  # 项目负责人工号
    JBR: str  # 经办人工号
    EDKZBM: str
    FY: str  # 附言
    JJFLKMBH: str
    FZRXM: str  # 项目负责人姓名
    JBRZJBH: str  # 经办人工号
    FIELD1: str  # 项目额度类型
    FIELD2: str  # 项目额度类型
    FIELD3: str
    FIELD4: str
    FIELD5: str
    FIELD6: str
    FIELD7: str
    FIELD8: str
    FIELD9: str
    FIELD10: str
    BXSY: str
    DWBH: str
    KSSH: str
    DJLX: str
    XMMC: str
    DJLY: str
    HTBH: str
    FPNR: str
    HSLXDM: str
    SX1: str
    SX2: str
    SX3: str
    BXQKSM: str
    CGLX: str
    NOHTBXQKSM: str
    ZCYWLXDM: str
    OASQH: str
    PLLSH: str
    EJXMBH: str
    ISWK: str
    SQSQDBH: str
    HTZXJHBH: str
    GJZ: str
    ISJSFACGHT: str
    JBRISBMZYFZR: str
    FIELD14: str
    JJFLKMMC: str
    ISCG: str
    ISYS: str
    ISGWK: str
    SQSQYSJE: str
    DZFPH: str
    JFLB: str
    JFLBMX: str
    HTBXQKSM: str
    FZMX: str
    LZZBJ: str
    ZBJJE: str
    ERJSON: str
    SPXXYWINFO: str
    SQDLXBH: str
    INVFYLX: str
    JELX: str
    BXSM: str
    FIELD20: str
    FIELD21: str
    FIELD22: str
    FIELD23: str
    FIELD24: str
    FIELD25: str
    ISWZH: str
    FIELD11: str
    FIELD12: str
    FIELD13: str
    FIELD15: str
    FIELD16: str
    FIELD17: str
    FIELD18: str
    FIELD19: str
    DPJEQR1W: str
    SQSQJFXX: str
    QUICKTYPE: str
    ISBHSWZCGZ: str


def get_reimbursement_by_reimbursement_id(reimbursement_id: str):
    """
    通过报销编号获取报销信息
    :param reimbursement_id: 报销编号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(Reimbursement).where(Reimbursement.YWBH == reimbursement_id and Reimbursement.JJE > 0)
        results = session.exec(statement).all()
        if results:
            return results


def get_reimbursement_by_operator_id(operator_id: str):
    """
    通过经办人编号获取报销信息
    :param operator_id: 经办人编号
    :return: 报销信息列表
    """
    with Session(reimbursement_engine) as session:
        statement = select(Reimbursement).where(Reimbursement.JBR == operator_id and Reimbursement.JJE > 0)

        results = session.exec(statement).all()
        if results:
            return results


def get_reimbursement_by_program_id(department_id: int, program_id: int):
    """
    通过部门编号获取报销信息
    :param department_id: 部门编号
    :return: 报销信息列表
    """
    department_id = int(department_id)
    program_id = int(program_id)
    with Session(reimbursement_engine) as session:
        statement = select(Reimbursement).where(
            Reimbursement.BMBH == department_id, Reimbursement.XMBH == program_id, Reimbursement.JJE > 0)

        results = session.exec(statement).all()
        if results:
            return results


def get_reimbursement_in_transit_by_program_id(department_id: int, program_id: int):
    """
    通过部门编号获取在途报销信息
    :param department_id: 部门编号
    :return: 报销信息列表
    """
    with Session(reimbursement_engine) as session:
        statement = select(Reimbursement).where(
            Reimbursement.BMBH == department_id and Reimbursement.XMBH == program_id and Reimbursement.JJE > 0 and Reimbursement.ZT != 3)

        results = session.exec(statement).all()
        if results:
            return results
