import io

import pandas as pd
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException
from service.indicator import find_null_values, process_indicators,get_indicators

router = APIRouter()


@router.post("/indicator/excel/")
async def indicator_excel(file: UploadFile = File(...)):
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
        df_input1 = pd.read_excel(io.BytesIO(contents))

        error_msg = find_null_values(df_input1)
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")

        insert_count, error_msg = process_indicators(df_input1)
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


@router.post("/indicator/list/")
async def indicator_list(year: str, page: int = 1, page_size: int = 20, indicator_name: str = ''):
    """
    获取指标列表
    """
    if not year:
        raise HTTPException(status_code=400, detail="年份为必填项")
    try:
        dict_indicators = get_indicators(year,page,page_size,indicator_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")
