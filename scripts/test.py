import sys
sys.path.append("../")
import json

import pytest

from tools.common_assert import common_assert
from tools.file_tool import FileTool
from tools.get_log import GetLog
from api.api import Api
from config import test_cases_file_name

log = GetLog.get_logger()


class Test01:
    # 1. 实例化获取工具类对象
    tool = FileTool(test_cases_file_name)

    # 2. 读取Excel ->将数据从excel中读取并写入到json文中
    tool.read_excel()

    # 3. 出参字典变量
    export_data = dict()

    # 3. 测试方法
    @pytest.mark.parametrize("case", tool.read_json())
    def test01(self, case):
        log.info("正在执行调用执行数据：{}".format(case))
        
        try:
            if "headers" in case:
                headers_str = json.dumps(case.get("headers"))
                for e in Test01.export_data:
                    headers_str = headers_str.replace(e, Test01.export_data[e])
                case["headers"] = json.loads(headers_str)

            if "params" in case:
                params_str = json.dumps(case.get("params"))
                for e in Test01.export_data:
                    params_str = params_str.replace(e, Test01.export_data[e])
                case["params"] = json.loads(params_str)

            # 调用 执行接口方法
            r = Api(case).run_method()
            # headers = r.headers
            # # print(headers["x-ca-request-id"])
            # log.info(headers)
            
            print("响应数据为：", r.text)
            print("响应状态码：", r.status_code)
            # 断言
            common_assert(r, case)
            # 将执行结果写入报告
            Test01.tool.write_excel(case.get("x_y"), "执行通过！")
            export_data = case.get("export_data")
            if export_data is not None:
                # 追加出参字典变量
                export_data_list = export_data.split("\n")
                if export_data_list is not None:
                    data = r.json()
                    for export_data in export_data_list:
                        key = export_data
                        find_keys_str = export_data[len("<<")-1 :-len(">>")].split(":")[1]
                        find_keys_str = find_keys_str.replace("[", "[\"")
                        find_keys_str = find_keys_str.replace("]", "\"]")
                        value = eval('data'+find_keys_str)
                        Test01.export_data[key] = value

        except Exception as e:
            Test01.tool.write_excel(case.get("x_y"), "执行失败！原因：{}".format(e))
            log.error("错误，原因：{}".format(e))
            raise
