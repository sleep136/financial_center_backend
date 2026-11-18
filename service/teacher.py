from models.Invoice import get_invoice_by_work_id, update_invoice_by_invoice_id
from models.InvoiceManagement import get_invoice_management_by_ygbh, update_ywbh_by_dzfph
from pydantic import BaseModel


def get_invoces(work_id,binding_status=0):
    # 从 YY_DZFP 表查询
    invoces = get_invoice_by_work_id(work_id, binding_status)
    invoce_list = []
    dzfph_set = set()  # 用于去重

    if invoces:
        for invoice in invoces:
            abstract = invoice.FPNR if invoice.FPNR else ""
            reservation_number = invoice.YYDH if invoice.YYDH else ""
            invoce_list.append(InvoceInfo(invoice_id=invoice.DZFPH, business_id=invoice.YWBH,
                                          work_id=invoice.JBR, reservation_number=reservation_number,
                                          billing_entity=invoice.KPDWMC, invoice_date=invoice.KPRQ,
                                          amount=invoice.ZJE, abstract=abstract
                                          ))
            dzfph_set.add(invoice.DZFPH)

    # 从 YY_DZFPGL 表查询（高铁/航空发票）
    management_invoices = get_invoice_management_by_ygbh(work_id)
    if management_invoices:
        for invoice in management_invoices:
            # 去重：如果 YY_DZFP 中已有该发票，则跳过
            if invoice.DZFPH in dzfph_set:
                continue
            # 只返回有出发地点和到达地点的（高铁/航空发票）
            if not invoice.CFDD and not invoice.DDDD:
                continue
            abstract = invoice.FPNR if invoice.FPNR else ""
            # YY_DZFPGL 没有 YYDH 字段，使用空字符串
            invoce_list.append(InvoceInfo(
                invoice_id=invoice.DZFPH,
                business_id=invoice.YWBH if invoice.YWBH else "",
                work_id=invoice.YGBH if invoice.YGBH else "",
                reservation_number="",
                billing_entity=invoice.DFDW if invoice.DFDW else "",
                invoice_date=invoice.KPRQ if invoice.KPRQ else "",
                amount=float(invoice.ZJE) if invoice.ZJE else 0.0,
                abstract=abstract
            ))
            dzfph_set.add(invoice.DZFPH)

    return invoce_list


def update_binging_status(invoice_id):
    """更新发票绑定状态，同时支持 YY_DZFP 和 YY_DZFPGL 两张表"""
    # 先尝试更新 YY_DZFP 表
    is_ok = update_invoice_by_invoice_id(invoice_id)
    if is_ok:
        return True
    # 如果 YY_DZFP 表没有该发票，尝试更新 YY_DZFPGL 表
    return update_ywbh_by_dzfph(invoice_id, "KS")


class InvoceInfo(BaseModel):
    invoice_id: str
    business_id: str
    work_id: str
    reservation_number: str
    billing_entity: str
    invoice_date: str
    amount: float
    abstract: str
