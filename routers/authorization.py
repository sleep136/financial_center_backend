from fastapi import APIRouter, HTTPException, status
from service.authorization import get_authorization_info_list_by_work_id,get_authorization_info_list_by_program_id

router = APIRouter()




@router.get("/authorization/teacher")
async def get_teacher_authorization(work_id: str):
    authorization = get_authorization_info_list_by_work_id(work_id)
    if not authorization:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return authorization


@router.get("/authorization/program")
async def get_program_authorization(program_id: str):
    authorization = get_authorization_info_list_by_program_id(program_id)
    if not authorization:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return authorization