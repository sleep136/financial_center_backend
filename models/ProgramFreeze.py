from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import financial_engine


class ProgramFreeze(SQLModel, table=True):
    """
    项目冻结明细
    """
    __tablename__ = "zw_xmdjmx"
    id: Optional[int] = Field(default=None, primary_key=True)
    rq: str  # 日期
    bmbh: Optional[str] = Field(default=None, primary_key=True)  # 部门编号
    xmbh: Optional[str] = Field(default=None, primary_key=True)  # 项目编号
    zy: str  # 摘要
    djje: float  # 冻结金额
    jdje: float  # 解冻金额
    lrr: str  # 录入人
    issh: str  # 是否审核
    shrq: str  # 审核日期
    shr: str  # 审核人
    pllsh: str  # 平台审核状态
    ywdh: str  # 业务编号
    sbr: str  # 提交人
    sbrq: str  # 提交日期
    lybh: str  # 来源编号
    yydh: str  # 业务编号
    xgr: str  # 对冲号
    xgrq: str  # 预约单号
    ywid: str  # 业务编号


def get_freeze_details(department_id: str, program_id: str):
    """
    通过项目编号获取项目信息，可能会查到多条
    :param program_id:
    :return:
    """
    with Session(financial_engine) as session:
        statement = select(ProgramFreeze).where(ProgramFreeze.xmbh == program_id, ProgramFreeze.bmbh == department_id)
        results = session.exec(statement).all()
        if results:
            return results
