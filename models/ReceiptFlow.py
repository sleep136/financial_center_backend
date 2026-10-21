from pydantic import BaseModel
from typing import Optional


class ReceiptFlowStatus(BaseModel):
    """接单流程状态"""
    sequence: int  # 序号
    source: str  # 流程来源
    handler: str  # 处理人
    remark: str  # 备注
    process_time: str  # 处理时间
    status: str  # 处理状态


class ReceiptFlowRecord(BaseModel):
    """接单管理记录"""
    id: int
    lx: str  # 类型
    jdrq: str  # 接单日期
    jdsj: str  # 接单时间
    jdr: str  # 接单人
    ywlsh: str  # 业务流水号
    jbr: str  # 经办人
    tel: str  # 电话
    bmbh: str  # 部门编号
    xmbh: str  # 项目编号
    je: float  # 金额
    zdr: str  # 制单人
    bz: str  # 备注
    zt: str  # 状态
    fdr: str  # 发单人
    qdr: str  # 签单人
    qdrdm: str  # 签单人代码
    qdsj: str  # 签单时间
    fhr: str  # 复核人
    fhrdm: str  # 复核人代码
    isfhfd: str  # 是否复核发送
    fhfdsj: str  # 复核发送时间
    yzdr: str  # 印章单人
    yzdrdm: str  # 印章单人代码
    pzbh: str  # 凭证编号
    pzrq: str  # 凭证日期
    pznm: str  # 凭证号码
    xtdm: str  # 系统代码
    fdsj: str  # 发送时间
    isfd: str  # 是否发送
    cwtdsm: str  # 财务退回说明

    class Config:
        from_attributes = True
