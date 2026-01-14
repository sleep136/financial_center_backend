from fastapi import APIRouter, HTTPException, status
from service.approval_workflow import get_workflow_by_work_id, get_workflow_by_business_id
router = APIRouter()


@router.get("/workflows/teacher")
async def get_workflow_list_by_work_id(work_id: str,state:int=-1):
    workflows = get_workflow_by_work_id(work_id,state)
    if not workflows:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return workflows


@router.get("/workflows/program")
async def get_workflow_list_by_business_id(business_id: str):
    workflows = get_workflow_by_business_id(business_id)
    if not workflows:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return workflows
