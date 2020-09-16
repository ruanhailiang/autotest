import os

# 1. 基路径
base_path = os.path.dirname(__file__)
# 2. 主机地址
# host = "localhost:8080"
host = "ford-cbz.emapgo.cn"
# 3. excel数据对应列
cell_config = {
    "protocol": 6,
    "path": 7,
    "method": 8,
    "headers": 9,
    "param_type": 10,
    "params": 11,
    "export_data": 12,
    "expect": 13,
    "is_run": 14,
    "result": 15,
    "passed": 16,
    "desc": 17
}

test_cases_file_name = "测试用例_deom.xlsx"
# 单元测试 or 集成测试
cases_sheet_name = "单元测试" 
variables_sheet_name = "environment"