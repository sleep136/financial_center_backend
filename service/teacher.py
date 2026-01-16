from models.Invoice import get_invoice_by_work_id, update_invoice_by_invoice_id
from pydantic import BaseModel


def get_invoces(work_id,binding_status=0):
    invoces = get_invoice_by_work_id(work_id,binding_status)
    invoce_list = []

    for invoice in invoces:
        abstract = invoice.FPNR if invoice.FPNR else ""
        reservation_number = invoice.YYDH if invoice.YYDH else ""
        invoce_list.append(InvoceInfo(invoice_id=invoice.DZFPH, business_id=invoice.YWBH,
                                      work_id=invoice.JBR, reservation_number=reservation_number,
                                      billing_entity=invoice.KPDWMC, invoice_date=invoice.KPRQ,

                                      amount=invoice.ZJE, abstract=abstract

                                      ))
    return invoce_list


def update_binging_status(invoice_id):
    return update_invoice_by_invoice_id(invoice_id)


class InvoceInfo(BaseModel):
    invoice_id: str
    business_id: str
    work_id: str
    reservation_number: str
    billing_entity: str
    invoice_date: str
    amount: float
    abstract: str
