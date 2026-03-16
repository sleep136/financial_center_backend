from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from service.budget import get_budget_breakdown

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/budget/one_program")
async def get_program(program_id: str, department_id: str, year: int):
    budgets = get_budget_breakdown(program_id, department_id, year)
    if not budgets:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return budgets
