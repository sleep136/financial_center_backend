from sqlmodel import SQLModel, Field, select, Session

from db import reimbursement_engine


class ApprovalWorkflow(SQLModel, table=True):
    __tablename__ = "TC_SPXXDL"
    __table_args__ = {'schema': "UAP"}
    PID: str = Field(primary_key=True)
    YWLSH: str  # 业务流水号
    MKDM: str  # 模块代码
    YWBH: str  # 业务编号
    TABLENAME: str
    SQR: str  # 申请人姓名
    SQRBH: str  # 申请人编号
    SQRQ: str  # 申请日期
    SQSJ: str  # 申请时间
    SQNR: str  # 申请内容摘要
    SPJB: str  # 审批级别
    SPR: str  # 审批人姓名
    SPRQ: str  # 审批日期
    SPSJ: str  # 审批时间
    SPSM: str  # 审批意见
    SPZT: str  # 审批状态  0未审批，1通过，2驳回
    CF1: str  # 是否收藏
    CF2: str  # 是否会签 0普通 1否 2是
    CF3: str  # 业务系统存取
    CF4: str  # 审批通用数据
    QMSJ: str
    TPXX: str
    SPRBH: str  # 审批人编号
    SIGNRESULT: str
    HANDWRITINGJSON: str
    SFQZ: str
    SFQM: str
    SPYZM: str
    TSDX: str
    YZM: str
    CWSP: str
    BJLC: str
    TSXX: str
    SPJS: str  # 审批角色名称
    CF5: str
    CF6: str
    CF7: str
    CF8: str
    CF9: str
    SCSPR: str
    ZDSPR: str
    SPJSBH: str
    INFO_PC: str
    INFO_MOBILE: str
    INFO_TYPE: str
    XZRBH: str
    SPRISNULL: str
    SIGNIMAGE: str
    GQ: str
    MD5: str
    CF10: str
    CF11: str
    CF12: str
    CF13: str
    CF14: str
    CF15: str
    CF16: str
    CF17: str
    CF18: str
    CF19: str
    CF20: str
    CF21: str
    CF22: str
    CF23: str
    CF24: str
    CF25: str
    CF26: str
    CF27: str
    CF28: str
    CF29: str


def get_approval_workflow_by_work_id(work_id: str):
    """
    通过工号获取工作流信息
    :param work_id: 工号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(ApprovalWorkflow).where(ApprovalWorkflow.SQRBH == work_id)
        results = session.exec(statement).all()
        if results:
            return results


def get_approval_workflow_by_business_id(business_id: str):
    """
    通过业务编号获取工作流信息
    :param business_id: 业务编号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(ApprovalWorkflow).where(ApprovalWorkflow.YWLSH == business_id)
        results = session.exec(statement).all()
        if results:
            return results
