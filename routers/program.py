from fastapi import APIRouter, HTTPException, status
from service.program import get_one_program, get_program_info_list, get_freeze_detail, get_reimbursement_detail, \
    get_labor_cost_detail,Reimbursement,LaborCost,VoucherDetail,get_economic_classification_cost
from fastapi.responses import JSONResponse
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/program/one_program")
async def get_program(program_id: str, department_id: str):
    programs = get_one_program(program_id, department_id)
    if not programs:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(status_code=200,
        content={"data": programs})


@router.get("/program/batch_program")
async def get_batch_program(program_id: str):
    program = get_program_info_list(program_id)
    if not program:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(status_code=200,
        content={"data": program})


@router.get("/program/freeze")
async def get_batch_freeze_detail(program_id: int, department_id: int):
    freeze_details = get_freeze_detail(program_id, department_id)
    if not freeze_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return freeze_details


@router.get("/program/reimbursement", response_model=list[Reimbursement])
async def get_batch_reimbursement_detail(program_id: str, department_id: str, filter_state: int=1):
    reimbursement_details = get_reimbursement_detail(program_id, department_id, filter_state)
    if not reimbursement_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return reimbursement_details


@router.get("/program/labor_cost", response_model=list[LaborCost])
async def get_batch_labor_cost_detail(program_id: str, department_id: str, filter_state: int=1):
    labor_cost_details = get_labor_cost_detail(program_id, department_id, filter_state)
    if not labor_cost_details:
        return []
    return labor_cost_details


@router.get("/program/economic_classification_cost", response_model=list[VoucherDetail])
async def get_economic_classification(program_id: str, department_id: str,  subject_code:str):
    economic_classification_details = get_economic_classification_cost(program_id, department_id, subject_code)
    if not economic_classification_details:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return economic_classification_details
