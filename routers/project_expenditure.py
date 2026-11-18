import io
import logging

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from models.ProjectExpenditure import ProjectExpenditureItem
from service.project_expenditure import parse_excel, save_to_redis, query_by_financial_code, get_all

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/project-expenditure/import", summary="上传Excel录入项目支出范围")
async def import_project_expenditure(file: UploadFile = File(...)):
    """
    上传 Excel 文件，解析后存入 Redis。
    Excel 需包含列：实施部门、财务编号、项目类型、项目名称、开支说明
    """
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="只支持 .xlsx 或 .xls 文件")

    try:
        contents = await file.read()
        df = pd.read_excel(
            io.BytesIO(contents),
            dtype=str,
            engine="openpyxl",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Excel 文件读取失败：{str(e)}")

    try:
        items = parse_excel(df)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        count = save_to_redis(items)
    except Exception as e:
        logger.error(f"写入 Redis 失败：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"数据写入失败：{str(e)}")

    return {"code": 200, "msg": f"成功导入 {count} 条记录", "count": count}


@router.get("/project-expenditure/query", summary="根据项目编号查询项目支出范围")
async def query_project_expenditure(keyword: str):
    """
    根据财务编号（项目编号）模糊查询项目支出范围。
    传空或不传则返回全部数据。
    """
    if not keyword or not keyword.strip():
        items = get_all()
    else:
        items = query_by_financial_code(keyword.strip())

    return {
        "code": 200,
        "count": len(items),
        "data": [item.model_dump() for item in items],
    }
