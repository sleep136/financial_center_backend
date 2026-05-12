from fastapi import APIRouter, HTTPException, status
from service.student import get_expense,get_accommodation_info,get_change_info

router = APIRouter()




@router.get("/student/expense")
async def get_student_expense(student_id: str):
    expense = get_expense(student_id)
    if not expense:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return expense

@router.get("/student/accommodation")
async def get_student_accommodation(student_id: str):
    accommodation_infos = get_accommodation_info(student_id)
    return accommodation_infos

@router.get("/student/change")
async def get_student_change_info(student_id: str):
    change_infos = get_change_info(student_id)
    return change_infos