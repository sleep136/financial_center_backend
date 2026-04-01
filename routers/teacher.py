from fastapi import APIRouter, HTTPException, status
from service.teacher import update_binging_status, get_invoces
from service.program import get_reimbursements_by_work_id, get_labor_costs_by_work_id,get_reimbursements_by_owner_id,get_labor_costs_by_owner_id

router = APIRouter()


@router.get("/invoice/list")
async def get_invoice_detail(work_id: str ,binding_status:int=0):
    invoces = get_invoces(work_id,binding_status)
    if not invoces:
        return []
    return invoces


@router.get("/invoice/unbind")
async def update_invoice_state(invoice_id: str):
    is_ok = update_binging_status(invoice_id)
    if not is_ok:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return is_ok

@router.get("/teacher/reimbursement")
async def get_reimbursement_by_user(work_id: str, filter_state: int = 1):
    reimbursements = get_reimbursements_by_work_id(work_id, filter_state)
    if not reimbursements:
        return []
    return reimbursements

@router.get("/teacher/labor_cost")
async def get_labor_cost_by_user(work_id: str, filter_state: int = 1):
    labor_costs = get_labor_costs_by_work_id(work_id, filter_state)
    if not labor_costs:
        return []
    return labor_costs

@router.get("/teacher/own_reimbursement")
async def get_reimbursement_by_owner(work_id: str, filter_state: int = 1):
    reimbursements = get_reimbursements_by_owner_id(work_id, filter_state)
    if not reimbursements:
        return []
    return reimbursements

@router.get("/teacher/own_labor_cost")
async def get_labor_cost_by_owner(work_id: str, filter_state: int = 1):
    labor_costs = get_labor_costs_by_owner_id(work_id, filter_state)
    if not labor_costs:
        return []
    return labor_costs