from fastapi import APIRouter, HTTPException, status
from service.receipt import get_recipe_info_list, get_recipe_urls

router = APIRouter()


@router.get("/receipe/get_receipes")
async def get_receipes(work_id: str = '', user_name: str = '', company_name: str = ''):
    if (not work_id) and (not user_name) and (not company_name):
        return []
    receipes = get_recipe_info_list(work_id, user_name, company_name)
    if not receipes:
        return []
    return receipes


@router.get("/receipe/get_receipe_url")
async def get_receipe_url(serial_num: str):
    receipe_url = get_recipe_urls(serial_num)
    if not receipe_url:
        return ''
    return receipe_url
