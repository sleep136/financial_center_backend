import json
import logging

import pandas as pd
from redis import Redis

from config.settings import settings
from models.ProjectExpenditure import ProjectExpenditureItem

logger = logging.getLogger(__name__)

REDIS_KEY = "project_expenditure"

redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)

COLUMN_MAPPING = {
    "实施部门": "department",
    "财务编号": "financial_code",
    "项目类型": "project_type",
    "项目名称": "project_name",
    "开支说明": "expenditure_desc",
}

REQUIRED_COLUMNS = list(COLUMN_MAPPING.keys())


def parse_excel(df: pd.DataFrame) -> list[ProjectExpenditureItem]:
    """解析 Excel DataFrame，返回项目支出记录列表"""
    df = df.dropna(how="all")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Excel 缺少必要列：{', '.join(missing)}")

    items: list[ProjectExpenditureItem] = []
    for idx, row in df.iterrows():
        financial_code = str(row.get("财务编号", "")).strip()
        if not financial_code or financial_code == "nan":
            continue

        items.append(ProjectExpenditureItem(
            department=str(row.get("实施部门", "")).strip(),
            financial_code=financial_code,
            project_type=str(row.get("项目类型", "")).strip(),
            project_name=str(row.get("项目名称", "")).strip(),
            expenditure_desc=str(row.get("开支说明", "")).strip(),
        ))

    if not items:
        raise ValueError("Excel 中没有有效数据行")

    return items


def save_to_redis(items: list[ProjectExpenditureItem]) -> int:
    """将记录列表写入 Redis Hash（以财务编号为 field），返回写入条数"""
    pipe = redis.pipeline()
    for item in items:
        pipe.hset(REDIS_KEY, item.financial_code, item.model_dump_json())
    pipe.execute()
    logger.info(f"项目支出范围写入 Redis 完成，共 {len(items)} 条")
    return len(items)


def query_by_financial_code(keyword: str) -> list[ProjectExpenditureItem]:
    """根据财务编号（项目编号）模糊查询，支持部分匹配"""
    all_data = redis.hgetall(REDIS_KEY)
    if not all_data:
        return []

    results: list[ProjectExpenditureItem] = []
    for field, value in all_data.items():
        if keyword in field:
            results.append(ProjectExpenditureItem(**json.loads(value)))
    return results


def get_all() -> list[ProjectExpenditureItem]:
    """获取全部项目支出范围数据"""
    all_data = redis.hgetall(REDIS_KEY)
    if not all_data:
        return []
    return [ProjectExpenditureItem(**json.loads(v)) for v in all_data.values()]
