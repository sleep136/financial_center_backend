from sqlmodel import SQLModel, Field, select, Session
from typing import Optional, List
from db import reimbursement_engine
from decimal import Decimal


class InvoiceManagement(SQLModel, table=True):
    """
    电子发票管理表（高铁/航空发票等）
    对应表: WSYY.YY_DZFPGL
    """
    __tablename__ = "YY_DZFPGL"
    __table_args__ = {'schema': "WSYY"}

    DZFPH: str = Field(default=None, primary_key=True)  # 电子发票号
    FPDM: Optional[str] = Field(default=None)  # 发票代码
    FPHM: Optional[str] = Field(default=None)  # 发票号码
    KPRQ: Optional[str] = Field(default=None)  # 开票日期
    YZM: Optional[str] = Field(default=None)  # 验证码
    GNFL: Optional[str] = Field(default=None)  # 功能分类
    ZT: Optional[str] = Field(default=None)  # 状态
    YWBH: Optional[str] = Field(default=None)  # 业务编号
    ZJE: Optional[str] = Field(default=None)  # 总金额
    TYPE: Optional[str] = Field(default=None)  # 类型
    JJFLKMBH: Optional[str] = Field(default=None)  # 经济分类科目编号
    DFDW: Optional[str] = Field(default=None)  # 对方单位
    CITY: Optional[str] = Field(default=None)  # 城市
    PRO: Optional[str] = Field(default=None)  # 省份
    DFYH: Optional[str] = Field(default=None)  # 对方银行
    DFZH: Optional[str] = Field(default=None)  # 对方账号
    FJID: Optional[str] = Field(default=None)  # 附件ID
    CFSJ: Optional[str] = Field(default=None)  # 出发时间
    DDSJ: Optional[str] = Field(default=None)  # 到达时间
    CFDD: Optional[str] = Field(default=None)  # 出发地点
    DDDD: Optional[str] = Field(default=None)  # 到达地点
    XM: Optional[str] = Field(default=None)  # 姓名
    CC: Optional[str] = Field(default=None)  # 车次/航班
    PB: Optional[str] = Field(default=None)  # 座位
    CJRQ: Optional[str] = Field(default=None)  # 创建日期
    YGBH: Optional[str] = Field(default=None)  # 员工编号
    FWLB: Optional[str] = Field(default=None)  # 服务类别
    TX_FILENAME: Optional[str] = Field(default=None)  # 附件名
    ZFFSBHLIST: Optional[str] = Field(default=None)  # 支付方式编号列表
    FZFJZS: Optional[int] = Field(default=0)  # 附件总数
    JBRMC: Optional[str] = Field(default=None)  # 经办人名称
    ZMRMC: Optional[str] = Field(default=None)  # 证明人名称
    BXLXBH: Optional[str] = Field(default=None)  # 报销类型编号
    ISYQ: Optional[str] = Field(default=None)  # 是否延期
    BMBH: Optional[str] = Field(default=None)  # 部门编号
    XMBH: Optional[str] = Field(default=None)  # 项目编号
    SZZSZT: Optional[str] = Field(default=None)  # 数字证书状态
    SZZSMSG: Optional[str] = Field(default=None)  # 数字证书消息
    BXJE: Optional[str] = Field(default=None)  # 报销金额
    SQJE: Optional[str] = Field(default=None)  # 申请金额
    SE: Optional[str] = Field(default=None)  # 税额
    FPNR: Optional[str] = Field(default=None)  # 发票内容
    INVINPUTTYPE: Optional[str] = Field(default=None)  # 发票输入类型
    PICKEY2: Optional[str] = Field(default=None)
    PICKEY3: Optional[str] = Field(default=None)
    FPLX: Optional[str] = Field(default=None)  # 发票类型
    KPNR: Optional[str] = Field(default=None)  # 开票内容
    ISYZ: Optional[str] = Field(default=None)  # 是否原始
    INV_SOURCE: Optional[str] = Field(default=None)  # 发票来源
    ZJE_TAX: Optional[str] = Field(default=None)  # 含税总金额
    ISCLFDZFP: Optional[str] = Field(default=None)  # 是否冲红电子发票
    UUID: Optional[str] = Field(default=None)
    FPLY: Optional[str] = Field(default=None)  # 发票来源
    LRR: Optional[str] = Field(default=None)  # 录入人
    CPH: Optional[str] = Field(default=None)  # 车牌号
    ZJH: Optional[str] = Field(default=None)  # 证件号
    SPFWMC: Optional[str] = Field(default=None)  # 服务名称
    SCSJ: Optional[str] = Field(default=None)  # 上传时间
    XCSJ: Optional[str] = Field(default=None)  # 修改时间
    ZIPFILEID: Optional[str] = Field(default=None)
    CHECKRESULT: Optional[str] = Field(default=None)  # 查验结果
    ZFBJ: Optional[str] = Field(default=None)  # 作废标记
    BZCLID: Optional[str] = Field(default=None)  # 标准策略ID
    BZCLTYPE: Optional[str] = Field(default=None)  # 标准策略类型
    JJFLKMMC: Optional[str] = Field(default=None)  # 经济分类科目名称
    CWZT: Optional[str] = Field(default=None)  # 财务状态
    ROUTEFILEID: Optional[str] = Field(default=None)
    COLLECT_BILL_NO: Optional[str] = Field(default=None)  # 集票号
    DANDUOLA_FILE_ID: Optional[str] = Field(default=None)
    CXSJ: Optional[str] = Field(default=None)  # 撤销时间


def get_invoice_management_by_ygbh(ygbh: str) -> List[InvoiceManagement]:
    """根据员工编号查询发票管理表"""
    with Session(reimbursement_engine) as session:
        statement = select(InvoiceManagement).where(InvoiceManagement.YGBH == ygbh)
        results = session.exec(statement).all()
        return results


def update_ywbh_by_dzfph(dzfph: str, ywbh: str) -> bool:
    """
    根据电子发票号更新业务编号

    Args:
        dzfph: 电子发票号
        ywbh: 新的业务编号

    Returns:
        bool: 更新是否成功
    """
    try:
        with Session(reimbursement_engine) as session:
            statement = select(InvoiceManagement).where(InvoiceManagement.DZFPH == dzfph)
            invoice = session.exec(statement).first()
            if not invoice:
                return False

            invoice.YWBH = ywbh
            session.add(invoice)
            session.commit()
            return True
    except Exception as e:
        print(f"更新发票管理表YWBH失败: {e}")
        return False
