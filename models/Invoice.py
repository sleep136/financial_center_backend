from sqlmodel import SQLModel, Field, select, Session
from typing import Optional
from db import reimbursement_engine


# 劳务相关

class Invoice(SQLModel, table=True):
    """
    发票
    """
    __tablename__ = "YY_DZFP"
    __table_args__ = {'schema': "WSYY"}
    DZFPH: str = Field(default=None, primary_key=True)  # 电子发票号
    FPDM: str  # 发票代码
    FPHM: str  # 发票号码
    HYFL: str
    SWLX: str
    KPRQ: str  # 开票日期
    FKFSBH: str
    FKDWMC: str
    FKDZDH: str
    FKKHH: str
    KPFSBH: str
    KPDWMC: str  # 开票单位名称
    KPDZDH: str  # 开票地址
    KPKHH: str  # 开票开户行
    JBR: str  # 经办人
    BZ: str
    YYDH: str  # 预约单号
    PZNM: str
    ZDR: str
    LRR: str  # 录入人
    LRRQ: str  # 录入日期
    LYBH: str
    KJND: str
    KJQJ: str
    PJLX: str
    BMBH: str
    XMBH: str
    ISBX: str
    FPNR: str
    JE: str  # 金额
    SE: str  # 税额
    ZJE: str  # 总金额
    YWBH: str  # 业务编号
    SL: str
    DJ: str
    YZM: str
    ISCHECK: str
    SSDQ: str
    MONGOFJNAME: str
    JSONSJ: str
    JSONSJ1: str
    JSON_CLOB: str
    ZMR: str
    BXLXBH: str
    JJFLKMBH: str
    SPZT: str
    SHSY: str
    DZPXJBZ: str
    MONGOFJNAME_ZIP: str
    SQBZSM: str
    LRSJ: str  # 录入时间
    SJLY: str
    ZFFSBHLIST: str
    FZFJZS: str
    JBRMC: str
    ZMRMC: str
    SQSQDBH: str


def get_invoice_by_work_id(work_id: str, binding_status=0) -> Optional[Invoice]:
    with Session(reimbursement_engine) as session:
        statement = select(Invoice).where(Invoice.JBR == work_id)
        if binding_status == 1:
            statement = statement.where(Invoice.YWBH != "KS")
        elif binding_status == 2:
            statement = statement.where(Invoice.YWBH == "KS")
        results = session.exec(statement).all()
        if results:
            return results


def update_invoice_by_invoice_id(invoice_id: str, bind_to_ks: bool = True) -> bool:
    """
    根据发票ID更新发票的业务编号(YWBH)字段

    Args:
        invoice_id: 电子发票号(DZFPH)
        bind_to_ks: 如果为True，则绑定到"KS"；如果为False，则取消绑定

    Returns:
        bool: 更新是否成功
    """
    try:
        with Session(reimbursement_engine) as session:
            # 查找对应的发票
            invoice = session.get(Invoice, invoice_id)
            if not invoice:
                return False

                # 更新YWBH字段
            if bind_to_ks:
                invoice.YWBH = "KS"  # 绑定到KS
            else:
                invoice.YWBH = None  # 取消绑定，可以设置为None或其他值

            # 提交更改到数据库
            session.commit()
            session.refresh(invoice)
            return True
    except Exception as e:
        print(f"更新发票失败: {e}")
        return False
