from sqlmodel import SQLModel, Field, select, Session, DateTime
from typing import Optional
from db import reimbursement_engine
from decimal import Decimal


class Receipt(SQLModel, table=True):  # 票据表
    __tablename__ = "YJPJ_SQ"
    __table_args__ = {'schema': "YJPJ"}
    ID: str = Field(primary_key=True)  # 申请流水号
    ADDRESS: str
    BAHTFKYY: str
    BCKPJE: str  # 开票金额
    BMBH: str  # 部门编号
    BZ: str     # 备注
    CAMPUS: str
    CAMPUS_CN: str
    CONTENT: str
    CREATE_TIME: str
    DCH: str
    DEPT: str
    DEPT_CHARGE: str
    DFDWMC: str  # 对方单位名称
    DJLSH: str
    DJXMBH: str
    EMAIL: str
    EXPIRE_DAYS: str
    FHR: str
    FIRST_AUDIT_TIME: str
    FKTJ: str
    FKTJMC: str
    FPZT: str
    FQEDJ: str
    FQEYY: str
    HTBH: str  # 合同编号
    HTDW: str
    HTJSSJ: str
    HTKSSJ: str
    HTZE: str
    HXR: str
    HXRQ: str
    INVALID: str
    ISAHTFK: str
    ISCKP: str
    ISDJ: str
    ISEQUAL: str
    ISHX: str
    ISONLINE: str
    ISSCKP: str
    ISSM: str
    ISSPXT: str
    ISTP: str
    ISXXM: str
    JKFS: str
    JKKSPZH: str
    JKRLX: str
    JKRLXMC: str
    JPRGZH: str   # 借票人工号
    JPRXM: str    # 借票人名称
    JSBMBH: str
    JSFSDM: str
    JSRDJE: str
    JYLSH: str
    KHH: str
    KKLSH: str
    KMBH: str
    KPLSH: str
    KPNR: str
    KPR: str
    KPZL: str
    KY_FLAG: str
    KYBH: str
    KYKPJE: str
    KYLX: str
    KYLXMC: str
    LAST_AUDIT_TIME: str
    MOBILE: str
    MSRDH: str
    NID: str
    NSRSBM: str
    ORDERNO: str
    PAYMETHOD: str
    PJLXDM: str
    PJLXMC: str  # 票据类型名称
    PJZT: str
    PRE_PROCESS_INSTANCE_ID: str
    PROCESS_INSTANCE_ID: str
    REASON: str  # 原因
    RET_CODE: str  # 结果编码
    RET_MSG: str  # 系统提示信息
    RETREAT_AUDIT_TIME: str
    RLLSH: str
    SKR: str
    SLBS: str
    START_DATE: str
    STATUS: str  # 状态
    TEL: str
    TRADENO: str
    UPDATE_TIME: str
    USER_DEPT: str
    USERID: str
    USERNAME: str
    XMBH: str
    XMLXMC: str
    XMMC: str
    YHZH: str
    YJDZRQ: str
    YKPJE: str
    YKPLSH: str
    YSYWH: str
    YWLX: str
    YXDW: str
    YZF: str
    YZP: str
    ZZS: str
    DEPT_CHARGE_CN: str
    DEPT_CN: str
    ISMS: str
    SUBMIT_TIME: str
    FJS: str
    QRMSG: str
    KPD: str
    BCKPCS: str
    KPZCS: str
    PZBH: str
    PZRQ: str
    ISMSZM: str
    ISSHBT: str
    JSR: str
    JSRGH: str
    LXDH: str
    RETREAT_SUBMIT_TIME: str
    TDYS_COUNT: str
    YWFLDM: str


class InvoiceInfo(SQLModel, table=True):  # 票据信息表
    __tablename__ = "YJPJ_KPJG"
    __table_args__ = {'schema': "YJPJ"}
    FPDM: str
    PJBH: str
    SQDLSH: str = Field(primary_key=True)  # 申请单流水号
    JE: str
    JKFS: str
    LY: str
    PJLXDM: str
    PJURL: str  # 票据地址
    YWRQ: str
    SE: str
    KPD: str
    OFDPICID: str
    PICID: str
    XMLPICID: str


def get_recipe(work_id: str = '', user_name: str = '', company_name: str = ''):
    """
    通过参数获取借票信息，可能会查到多条
    :param work_id: 工作ID
    :param user_name: 用户姓名
    :param company_name: 公司名称（支持模糊搜索）
    :return: 匹配的借票信息列表
    """
    with Session(reimbursement_engine) as session:
        # 初始化基础查询
        statement = select(Receipt)

        # 逐个添加过滤条件（不会互相覆盖，多条件同时生效）
        if work_id:
            statement = statement.where(Receipt.USERID == work_id)
        if user_name:
            statement = statement.where(Receipt.USERNAME == user_name)
        if company_name:
            # 关键修改：模糊查询，包含company_name即可匹配
            statement = statement.where(Receipt.DFDWMC.like(f"%{company_name}%"))
        statement = statement.order_by(Receipt.CREATE_TIME.desc())
        # 执行查询
        results = session.exec(statement).all()

        return results  # 空列表直接返回即可，无需判断

def get_recipe_url(serial_num):
    with Session(reimbursement_engine) as session:
        # 初始化基础查询
        statement = select(InvoiceInfo)

        # 逐个添加过滤条件（不会互相覆盖，多条件同时生效）

        statement = statement.where(InvoiceInfo.SQDLSH == serial_num)


        # 执行查询
        results = session.exec(statement).first()

        return results  # 空列表直接返回即可，无需判断
