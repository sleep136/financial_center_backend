import logging
import pandas as pd
from models.Voucher import (get_breakdown_by_department_program_id, get_date_by_voucher_id,
                            get_breakdown_total_amount_by_department_program_id)
from models.Program import get_program_by_xmbh_exact_3digits
from pydantic import BaseModel
import os
import datetime

logger = logging.getLogger(__name__)


def get_budget_breakdown(program_id: str, department_id: str, year: int = 2026,
                         start_month: str = '0', end_month: str = '13'):
    """
    获取项目劳务成本明细
    :param program_id:
    :param department_id:
    :return:
    """

    department_id = str(department_id)
    program_id = str(program_id)

    voucher_results = get_breakdown_by_department_program_id(department_id, program_id, year)

    if not voucher_results:
        return False
    list_pznm_id = []
    for voucher_result in voucher_results:
        list_pznm_id.append(voucher_result.pznm)
    list_pznm_id = list(set(list_pznm_id))
    budget_date_list = get_date_by_voucher_id(list_pznm_id, year)
    dict_budget_date = {}
    for budget_date in budget_date_list:
        dict_budget_date[budget_date.pznm] = budget_date
    list_voucher_detail = []
    for vocher in voucher_results:
        vocher_detail = dict_budget_date[vocher.pznm]
        if int(vocher_detail.kjqj) > int(end_month) or int(vocher_detail.kjqj) < int(start_month):
            continue
        voucher_id = vocher_detail.pzbh
        type_id = vocher_detail.lxbh
        date = vocher_detail.pzrq
        list_voucher_detail.append(VoucherDetail(voucher_number='(' + str(type_id) + ')' + str(voucher_id),
                                                 voucher_date=date[:4] + "-" + date[4:6] + '-' + date[6:8],
                                                 program_id=program_id,
                                                 department_id=vocher.bmbh,
                                                 abstract=vocher.zy,
                                                 operator=vocher_detail.xgr,
                                                 amount=vocher.dje
                                                 ))
    return list_voucher_detail


def fetch_subprojects_for_parents(df_parents, year, xmbh_col='项目编号', bmbh_col='部门编号'):
    """
    为每个父项目查询其子项目

    参数:
        df_parents: 包含父项目的DataFrame
        xmbh_col: 项目编号列名
        bmbh_col: 部门编号列名

    返回:
        包含父项目和子项目的完整DataFrame
    """
    all_projects = []  # 存储所有项目（父+子）

    # 先添加所有父项目
    for _, row in df_parents.iterrows():
        # 已下发预算金额
        val = get_breakdown_total_amount_by_department_program_id(int(row[bmbh_col]), int(row[xmbh_col]),year)
        # 兼容NULL/空值
        if val is None or val == "":
            issued_budget_amount = 0.0
        else:
            issued_budget_amount = float(val)

        parent_project = {
            '部门编号': row[bmbh_col],
            '项目编号': row[xmbh_col],
            '预算金额': row['预算金额'],
            '50%金额': row['50%金额'],
            '25%金额': row['25%金额'],
            '已下达预算金额':issued_budget_amount,
            "还未下达": row['预算金额']-issued_budget_amount,
            "已下达占全年比例": f"{issued_budget_amount/row['预算金额']:.0%}",
            '层级': '父项目',
            '父项目编号': None,  # 父项目本身没有父项目
            '来源Sheet': row.get('来源Sheet', 'Excel'),
        }
        all_projects.append(parent_project)

        # 调用数据库查询子项目
        try:
            # 使用父项目编号作为前缀查询子项目
            subprojects = get_program_by_xmbh_exact_3digits(
                bmbh=row[bmbh_col],
                xmbh_prefix=row[xmbh_col],
                year=year

            )

            # 将查询到的子项目添加到列表
            for sp in subprojects:
                # 从数据库对象中提取数据（根据您的实际模型调整）
                subproject = {
                    '部门编号': sp.bmbh,  # 假设数据库字段名
                    '项目编号': sp.xmbh,
                    '预算金额': sp.ysje if hasattr(sp, 'ysje') else 0,  # 假设预算金额字段
                    '50%金额': (sp.ysje * 0.5) if hasattr(sp, 'ysje') else 0,
                    '25%金额': (sp.ysje * 0.25) if hasattr(sp, 'ysje') else 0,
                    '层级': '子项目',
                    '父项目编号': row[xmbh_col],
                    '来源Sheet': '数据库',
                }
                all_projects.append(subproject)

            print(f"父项目 {row[xmbh_col]} 查询到 {len(subprojects)} 个子项目")

        except Exception as e:
            print(f"查询父项目 {row[xmbh_col]} 的子项目失败: {e}")

    # 转换为DataFrame
    result_df = pd.DataFrame(all_projects)
    return result_df


def create_hierarchical_display(df, project_col='项目编号'):
    """
    创建层级显示的DataFrame，带缩进和图标
    """
    df_display = df.copy()

    # 创建显示用的项目编号列（带缩进）
    def format_project_code(row):
        if row['层级'] == '父项目':
            return f"📁 {row[project_col]}"
        else:
            return f"  ├─ {row[project_col]}"

    df_display['显示项目编号'] = df_display.apply(format_project_code, axis=1)

    # 按父项目编号排序，使同一父项目的子项目聚集在一起
    df_display = df_display.sort_values(
        by=['父项目编号', '层级'],
        na_position='first'
    )

    return df_display


def read_excel_with_subprojects(file_path, required_columns, year):
    """
    读取Excel文件，获取父项目，然后从数据库查询子项目
    """
    # 第一步：读取Excel（只包含父项目）
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names

    df_list = []

    for sheet in sheet_names:
        df_sheet = pd.read_excel(file_path, sheet_name=sheet)

        # 检查必需的列
        missing_cols = [col for col in required_columns if col not in df_sheet.columns]
        if missing_cols:
            print(f"警告: Sheet '{sheet}' 缺少列 {missing_cols}，跳过该 sheet")
            continue

        # 提取需要的列
        df_subset = df_sheet[required_columns].copy()

        # 转换预算金额为数值
        df_subset['预算金额'] = pd.to_numeric(df_subset['预算金额'], errors='coerce')

        # 计算50%和25%金额
        df_subset['50%金额'] = df_subset['预算金额'] * 0.5
        df_subset['25%金额'] = df_subset['预算金额'] * 0.25

        # 添加来源标识
        df_subset['来源Sheet'] = sheet

        df_list.append(df_subset)
        print(f"已读取 Sheet '{sheet}'，共 {len(df_subset)} 个父项目")

    # 合并所有父项目
    if not df_list:
        print("未读取到任何有效数据")
        return pd.DataFrame()

    parent_df = pd.concat(df_list, ignore_index=True)
    print(f"\n共读取 {len(parent_df)} 个父项目")

    # 第二步：查询子项目
    print("\n开始查询子项目...")
    full_df = fetch_subprojects_for_parents(parent_df, year)

    return full_df


def analyze_and_display(df):
    """
    分析和展示项目层级结构
    """
    print("\n" + "=" * 70)
    print("项目结构分析报告")
    print("=" * 70)

    # 统计信息
    parent_count = df[df['层级'] == '父项目'].shape[0]
    child_count = df[df['层级'] == '子项目'].shape[0]

    print(f"父项目数: {parent_count}")
    print(f"子项目数: {child_count}")
    print(f"项目总数: {len(df)}")

    # 预算统计
    total_parent_budget = df[df['层级'] == '父项目']['预算金额'].sum()
    total_child_budget = df[df['层级'] == '子项目']['预算金额'].sum()

    print(f"\n预算统计:")
    print(f"父项目预算总额: {total_parent_budget:,.2f}")
    print(f"子项目预算总额: {total_child_budget:,.2f}")
    print(f"总预算: {total_parent_budget + total_child_budget:,.2f}")

    # 创建层级展示
    display_df = create_hierarchical_display(df)

    # 选择显示的列
    show_columns = ['显示项目编号', '部门编号', '预算金额', '50%金额', '25%金额', '层级', '来源Sheet']
    show_columns = [col for col in show_columns if col in display_df.columns]

    print("\n" + "=" * 70)
    print("层级展示表格")
    print("=" * 70)
    print(display_df[show_columns].to_string(index=False))

    # 按父项目汇总
    print("\n" + "=" * 70)
    print("按父项目汇总（包含子项目）")
    print("=" * 70)

    summary_data = []
    for parent_id in df[df['层级'] == '父项目']['项目编号'].unique():
        parent_row = df[df['项目编号'] == parent_id].iloc[0]
        children = df[df['父项目编号'] == parent_id]

        summary_data.append({
            '父项目编号': parent_id,
            '部门编号': parent_row['部门编号'],
            '父项目预算': parent_row['预算金额'],
            '子项目数量': len(children),
            '子项目总预算': children['预算金额'].sum() if not children.empty else 0,
            '总预算': parent_row['预算金额'] + (children['预算金额'].sum() if not children.empty else 0)
        })

    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))

    return display_df


def generate_budget_implementation_efficiency(year: int):
    """
    生成预算执行率
    :return:
    """
    required_columns = ['部门编号', '项目编号', '预算金额']
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 获取父级目录
    parent_dir = os.path.dirname(current_dir)
    file_path = str(year) + '预算执行情况.xlsx'
    template_file_path = os.path.join(parent_dir, "static", file_path)

    xls = pd.ExcelFile(template_file_path)
    sheet_names = xls.sheet_names

    # 存储每个 sheet 提取后的 DataFrame

    full_df = read_excel_with_subprojects(template_file_path, required_columns, year)

    if full_df.empty:
        print("没有数据")
        return

    # 分析和展示
    display_df = analyze_and_display(full_df)

    print(display_df.head())


class VoucherDetail(BaseModel):
    voucher_date: str
    voucher_number: str
    program_id: int
    department_id: int
    abstract: str
    amount: float
    operator: str
