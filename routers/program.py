from fastapi import APIRouter, HTTPException, status
from service.program import get_one_program, get_program_info_list, get_freeze_detail, get_reimbursement_detail, \
    get_labor_cost_detail

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/program/one_program")
async def get_program(program_id: str, department_id: str):
    programs = get_one_program(program_id, department_id)
    if not programs:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return programs


@router.get("/program/batch_program")
async def get_batch_program(program_id: str):
    program = get_program_info_list(program_id)
    if not program:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return program


@router.get("/program/freeze")
async def get_batch_freeze_detail(program_id: int, department_id: int):
    freeze_details = get_freeze_detail(program_id, department_id)
    if not freeze_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return freeze_details


@router.get("/program/reimbursement")
async def get_batch_reimbursement_detail(program_id: str, department_id: str):
    reimbursement_details = get_reimbursement_detail(program_id, department_id)
    if not reimbursement_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return reimbursement_details


@router.get("/program/labor_cost")
async def get_batch_labor_cost_detail(program_id: str, department_id: str):
    labor_cost_details = get_labor_cost_detail(program_id, department_id)
    if not labor_cost_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return labor_cost_details
