from fastapi import APIRouter, HTTPException, status
from service.program import get_one_program, get_program_info_list

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/program/")
async def get_program(program_id: str, department_id: str):
    programs = get_one_program(program_id,department_id)
    if not programs:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return programs


@router.get("/program/")
async def get_batch_program(program_id: str):
    program = get_program_info_list(program_id)
    if not program:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return program
