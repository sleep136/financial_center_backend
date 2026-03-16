import io
import os

import pandas as pd
from fastapi import APIRouter
from fastapi import File, UploadFile
from fastapi import HTTPException
from fastapi.responses import FileResponse

from service.indicator import find_null_values, process_indicators, get_indicators, process_compare_indicators

router = APIRouter()


@router.post("/indicator/process-import")
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
        df_input1 = pd.read_excel(
            io.BytesIO(contents),
            dtype=str,  # 所有列作为字符串
            engine='openpyxl'  # 明确指定引擎（对于.xlsx文件）
        )

        error_msg = find_null_values(df_input1)
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")

        insert_count, error_msg = process_indicators(df_input1)
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")
        return 'ok'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


@router.get("/indicator/list")
async def indicator_list(budget_year: str, page: int = 1, page_size: int = 20, keyword: str = ''):
    """
    获取指标列表
    """
    if not budget_year:
        raise HTTPException(status_code=400, detail="年份为必填项")
    try:
        dict_indicators = get_indicators(budget_year, page, page_size, keyword)
        return dict_indicators
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


@router.post("/indicator/process-compare")
async def indicator_compare_excel(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """
    上传Excel文件并读取为DataFrame
    """
    # 检查文件类型
    if not file1.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 或 .xls 文件")
    if not file2.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 或 .xls 文件")
    try:
        # 读取文件内容
        contents1 = await file1.read()

        # 使用pandas读取Excel
        df_input1 = pd.read_excel(io.BytesIO(contents1))

        contents2 = await file2.read()
        # 使用pandas读取Excel
        df_input2 = pd.read_excel(io.BytesIO(contents2))
        try:
            insert_count, error_msg = process_compare_indicators(df_input1, df_input2)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{str(e)}")
        if error_msg:
            raise HTTPException(status_code=500, detail=f"{error_msg}")
        return 'ok'
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


@router.get("/indicator/template")
async def indicator_excel_template():
    """
    下载Excel模板文件
    """
    try:
        # 获取当前文件所在的目录（假设路由文件在项目的某个子目录中）
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 获取父级目录
        parent_dir = os.path.dirname(current_dir)

        # 构建模板文件路径
        template_file_path = os.path.join(parent_dir, "static", "上传指标模板文件.xlsx")

        # 检查文件是否存在
        if not os.path.exists(template_file_path):
            raise HTTPException(
                status_code=404,
                detail="模板文件不存在"
            )

        # 返回文件响应
        return FileResponse(
            path=template_file_path,
            filename="指标上传模板.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"下载模板文件失败: {str(e)}"
        )
