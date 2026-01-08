from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import reimbursement_engine


class Authorization(SQLModel, table=True):
    __tablename__ = "WEB_XMSQSYLOG"
    __table_args__ = {'schema': "GGK"}
    LOGID: str = Field(primary_key=True)
    BMBH: str = Field(default=None)  # 部门编号
    XMBH: str = Field(default=None)  # 项目编号
    SQRZJH: str = Field(default=None)  # 授权人账号
    BSQRZJH: str = Field(default=None)  # 被授权人账号
    MSYSTEM: str = Field(default=None)  # 系统id
    MOPERATE: str = Field(default=None)  # 操作名称
    MCZRQ: str = Field(default=None)  # 操作时间
    MIP: str = Field(default=None)  # 操作IP
    SQJE: float = Field(default=None)  # 授权金额
    QXJE: float = Field(default=None)  # 取消金额
    YSQRZID: str = Field(default=None)  # 原授权ID
    QXFLG: str = Field(default=None)  # 0：代表该log是取消操作，1：原log已取消，2：原log未取消
    XMMC: str = Field(default=None)  # 项目名称
    MAC: str = Field(default=None)  # 操作MAC
    ZTDM: str = Field(default=None)  # 状态代码


def get_authorization_by_program_id(program_id: str):
    """
    通过项目编号获取授权信息
    :param program_id: 项目编号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(Authorization).where(Authorization.XMBH == program_id)
        results = session.exec(statement).all()
        if results:
            return results

def get_authorization_by_work_id(work_id: str):
    """
    通过被授权人账号获取授权信息
    :param work_id: 被授权人账号
    :return:
    """
    with Session(reimbursement_engine) as session:
        statement = select(Authorization).where(Authorization.BSQRZJH == work_id)
        results = session.exec(statement).all()
        if results:
            return results