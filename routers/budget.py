from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import io
from service.budget import get_budget_breakdown, find_null_values, get_budget_stats
import pandas as pd
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi import HTTPException

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.get("/budget/one_program")
async def get_program(program_id: str, department_id: str, year: int, start_month: str, end_month: str):
    budgets = get_budget_breakdown(program_id, department_id, year, start_month, end_month)
    if not budgets:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return budgets


@router.get("/budget/programs")
async def get_batch_programs(file: UploadFile = File(...)):
    """
    上传Excel文件并读取为DataFrame
    """
    # 检查文件类型
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 或 .xls 文件")

    try:
        # 读取文件内容
        contents = await file.read()

        # 使用pandas读取Excel
        df_input1 = pd.read_excel(
            io.BytesIO(contents),
            dtype=str,  # 所有列作为字符串
            engine='openpyxl'  # 明确指定引擎（对于.xlsx文件）
        )

        error_msg = find_null_values(df_input1)
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")

        list_count, list_error_msg = get_budget_stats(df_input1)


        return {"data":list_count,"error_list":list_error_msg}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")
