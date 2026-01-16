from fastapi import APIRouter, HTTPException, status
from service.teacher import update_binging_status, get_invoces

router = APIRouter()


@router.get("/invoice/list")
async def get_invoice_detail(work_id: str ,binding_status:int=0):
    invoces = get_invoces(work_id,binding_status)
    if not invoces:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return invoces


@router.get("/invoice/unbind")
async def update_invoice_state(invoice_id: str):
    is_ok = update_binging_status(invoice_id)
    if not is_ok:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return is_ok
