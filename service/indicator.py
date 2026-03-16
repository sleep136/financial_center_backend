import logging
import pandas as pd
from models.Indicator import insert_indicators, check_zbdm_exists, get_batch_indicators
from pydantic import BaseModel
import datetime

logger = logging.getLogger(__name__)

DICT_GOVERNMENT_BUDGET_TO_DEPARTMENTAL_BUDGET_EXPENDITURE = {50501: [30101,
                                                                     30102,
                                                                     30103,
                                                                     30106,
                                                                     30107,
                                                                     30108,
                                                                     30109,
                                                                     30110,
                                                                     30111,
                                                                     30112,
                                                                     30113,
                                                                     30114,
                                                                     30199],
                                                             50502: [30201,
                                                                     30202,
                                                                     30204,
                                                                     30205,
                                                                     30206,
                                                                     30207,
                                                                     30208,
                                                                     30209,
                                                                     30211,
                                                                     30212,
                                                                     30213,
                                                                     30214,
                                                                     30215,
                                                                     30216,
                                                                     30217,
                                                                     30218,
                                                                     30219,
                                                                     30225,
                                                                     30226,
                                                                     30227,
                                                                     30228,
                                                                     30231,
                                                                     30239,
                                                                     30240,
                                                                     30299],
                                                             50905: [30301],
                                                             50999: [30302, 30303, 30305, 30306, 30307, 30309, 30399],
                                                             50901: [30304],
                                                             50902: [30308],
                                                             50601: [31001,
                                                                     31002,
                                                                     31003,
                                                                     31005,
                                                                     31006,
                                                                     31007,
                                                                     31008,
                                                                     31009,
                                                                     31010,
                                                                     31011,
                                                                     31012,
                                                                     31013,
                                                                     31014,
                                                                     31021,
                                                                     31022,
                                                                     31099]}


def process_indicators(df_input1):
    list_input1 = []

    for index, item in df_input1.iterrows():

        for government_budget_expenditure_economic_classification, list_departmental_budget_expenditure_economic_classification in DICT_GOVERNMENT_BUDGET_TO_DEPARTMENTAL_BUDGET_EXPENDITURE.items():

            for departmental_budget_expenditure_economic_classification in list_departmental_budget_expenditure_economic_classification:
                budget_indicator_code = str(item['指标ID']) + '-' + str(
                    government_budget_expenditure_economic_classification) + '-' + str(
                    departmental_budget_expenditure_economic_classification)
                logger.info(f"""
                '预算指标代码': {budget_indicator_code},
                             '预算指标名称': {item['指标名称']},
                             '预算年度': {item['预算年度']},
                             '财政预算项目代码': {item["预算项目代码"]},
                             '政府支出经济分类': {str(government_budget_expenditure_economic_classification)}
                             '部门支出经济分类': {str(departmental_budget_expenditure_economic_classification)}
                             '本级指标文号': {item["指标文号"]},
                             '资金性质代码': {item["资金性质编码"]},
                             '支出功能分类': {item["功能分类"]}
                             '指标类型代码': {item["指标类型编码"]}
                             '集中支付科目编号':{item["零余额科目"]}
                             '财政标准代码': {budget_indicator_code}
                             '是否启用': {"1"}
                             '指标金额': {"999999999"}
                             '指标余额': {"999999999"}
                             """)
                dict_temp = {'预算指标代码': budget_indicator_code,
                             '预算指标名称': item['指标名称'],
                             '预算年度': item['预算年度'],
                             '财政预算项目代码': item["预算项目代码"],
                             '政府支出经济分类': str(government_budget_expenditure_economic_classification),
                             '部门支出经济分类': str(departmental_budget_expenditure_economic_classification),
                             '本级指标文号': item["指标文号"],
                             '资金性质代码': item["资金性质编码"],
                             '支出功能分类': item["功能分类"],
                             '指标类型代码': item["指标类型编码"],
                             '集中支付科目编号': item["零余额科目"],
                             '财政标准代码': budget_indicator_code,
                             '是否启用': "1",
                             '指标金额': "999999999",
                             '指标余额': "999999999", }
                list_input1.append(dict_temp)
    dict_check = check_zbdm_exists([item['预算指标代码'] for item in list_input1])
    if dict_check["exists"]:
        msg = f'指标：{dict_check["exists"]}已存在 '
        return 0, msg
    count, msg = insert_indicators(list_input1)
    return count, msg


def find_null_values(df):
    """
    查找并返回所有空值的详细位置
    """
    null_info = []

    # 遍历DataFrame的每一行
    for idx, row in df.iterrows():
        indicator_id = row['指标ID']  # 获取指标ID
        null_cols = []

        # 检查该行各列是否为空
        for col in df.columns:
            if pd.isna(row[col]):
                null_cols.append(col)

        # 如果该行有空值，记录信息
        if null_cols:
            null_info.append({
                '指标ID': indicator_id,
                '空值列': null_cols,
                '空值数量': len(null_cols),
                '行索引': idx
            })

    return null_info


def get_indicators(year: str, page: int = 1, page_size: int = 20, indicator_name: str = ''):
    dict_batch_indicators = get_batch_indicators(year, page, page_size, indicator_name)
    list_indicators = []
    for indicator in dict_batch_indicators['data']:
        list_indicators.append({
            "indicator_code": indicator.Zbdm,
            "indicator_name": indicator.Zbmc,
            "fiscal_year": indicator.ysnd,
            "fiscal_budget_project_code": indicator.Gkxmdm,
            "economic_classification_of_government_expenditures": indicator.gkjjfldm,
            "economic_classification_of_departmental_expenditures": indicator.jjflkmbh,
            "indicator_number": indicator.Zbwh,
            "fund_nature_code": indicator.Zjxzdm,
            "classification_of_expenditure_functions": indicator.Lkx,
            "indicator_type_code": indicator.Zblxdm,
            "centralized_payment_account_number": indicator.kmbh,
            "fiscal_standard_code": indicator.czbzdm,
            "is_enable": indicator.isqy,
            "indicator_amount": indicator.Zbje,
            "indicator_balance": indicator.Zbye,
        })
    dict_batch_indicators['data'] = list_indicators
    return dict_batch_indicators


def process_compare_indicators(df_input1, df_input2):
    # 检查df2中是否有重复的指标额度ID
    duplicate_ids = df_input2['指标额度ID'][df_input2['指标额度ID'].duplicated()].unique()
    if len(duplicate_ids) > 0:
        raise ValueError(f"df2中存在重复的指标额度ID: {list(duplicate_ids)}")

    # 执行左连接
    merged_df = pd.merge(
        df_input1[['指标ID',	'指标文号','功能分类编码']],
        df_input2[['指标额度ID', '预算项目代码', '预算项目名称']],
        how='left',
        left_on='指标ID',
        right_on='指标额度ID'
    )

    # 检查是否有未匹配的指标ID
    missing_ids = merged_df[merged_df['指标额度ID'].isna()]['指标ID'].unique()
    if len(missing_ids) > 0:
        raise ValueError(f"df2中未找到对应的指标额度ID: {list(missing_ids)}")

    error_msg = find_null_values(merged_df)
    if error_msg:
        raise ValueError(f"{error_msg}")
            # 读取文件内容
    # 可以选择删除临时的连接键列（如果需要）
    # merged_df = merged_df.drop('指标额度ID', axis=1)
    # 方法1：使用datetime.now()
    current_year = datetime.datetime.now().year

    list_input1 = []
    for index, item in merged_df.iterrows():

        for government_budget_expenditure_economic_classification, list_departmental_budget_expenditure_economic_classification in DICT_GOVERNMENT_BUDGET_TO_DEPARTMENTAL_BUDGET_EXPENDITURE.items():

            for departmental_budget_expenditure_economic_classification in list_departmental_budget_expenditure_economic_classification:
                budget_indicator_code = str(item['指标ID']) + '-' + str(
                    government_budget_expenditure_economic_classification) + '-' + str(
                    departmental_budget_expenditure_economic_classification)
                logger.info(f"""
                '预算指标代码': {budget_indicator_code},
                             '预算指标名称': {item['预算项目名称']},
                             '预算年度': {current_year},
                             '财政预算项目代码': {item["预算项目代码"]},
                             '政府支出经济分类': {str(government_budget_expenditure_economic_classification)}
                             '部门支出经济分类': {str(departmental_budget_expenditure_economic_classification)}
                             '本级指标文号': {item["指标文号"]},
                             '资金性质代码': '1111',
                             '支出功能分类': {item["功能分类编码"]}
                             '指标类型代码': '211'
                             '集中支付科目编号':'1011'
                             '财政标准代码': {budget_indicator_code}
                             '是否启用': {"1"}
                             '指标金额': {"999999999"}
                             '指标余额': {"999999999"}
                             """)
                dict_temp = {'预算指标代码': budget_indicator_code,
                             '预算指标名称': item['预算项目名称'],
                             '预算年度': current_year,
                             '财政预算项目代码': item["预算项目代码"],
                             '政府支出经济分类': str(government_budget_expenditure_economic_classification),
                             '部门支出经济分类': str(departmental_budget_expenditure_economic_classification),
                             '本级指标文号': item["指标文号"],
                             '资金性质代码': '1111',
                             '支出功能分类': item["功能分类编码"],
                             '指标类型代码': '211',
                             '集中支付科目编号': '1011',
                             '财政标准代码': budget_indicator_code,
                             '是否启用': "1",
                             '指标金额': "999999999",
                             '指标余额': "999999999", }
                list_input1.append(dict_temp)

    dict_check = check_zbdm_exists([item['预算指标代码'] for item in list_input1])
    if dict_check["exists"]:
        msg = f'指标：{dict_check["exists"]}已存在 '
        return 0, msg
    count, msg = insert_indicators(list_input1)
    return count, msg
