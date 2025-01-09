from fastapi import APIRouter, HTTPException, status
from service.student import get_expense

router = APIRouter()




@router.get("/student/expense")
async def get_student_expense(student_id: str):
    expense = get_expense(student_id)
    if not expense:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return expense

