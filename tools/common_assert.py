import re
import deepdiff
from tools.get_log import GetLog

log = GetLog.get_logger()


def common_assert(response, case):
    expect = case.get("expect")
    # 01 断言 响应状态吗
    assert response.status_code == expect.get("code"), "错误！响应 code：{} 预期code：{}".format(response.status_code,
                                                                                        expect.get("code"))

    expect_result = expect.get("result")
    if expect_result is None:
        assert response.text == '', "错误！响应 result：{} 预期 result：{}".format(response.text, expect_result)
        return
    log.info("正在调用断言公共方法")
    # 获取响应数据
    try:
        result = response.json()
    except:
        raise Exception("输出结果为空，不符合约定的规范")

    # 断言 data
    data = result.get("data")
    expect_data = expect_result.get("data")
    assert type(data) == type(expect_data), "错误！响应 data：{} 预期 data：{}".format(data, expect_data)

    is_matched = True
    if type(data) == type(expect_data):
        diff = dict(deepdiff.DeepDiff(expect_data, data))
        if "dictionary_item_added" in diff or "dictionary_item_removed" in diff:
            is_matched = False
        elif "values_changed" in diff:
            values_changed = diff["values_changed"]
            for key in values_changed:
                values = values_changed[key]
                expect_data_value = values["old_value"]
                data_value = values["new_value"]
                if expect_data_value == data_value:
                    continue
                if type(expect_data_value) != str:
                    is_matched = False
                    break
                if not expect_data_value.startswith("{{") and expect_data_value.endswith("}}"):
                    is_matched = False
                    break
                if type(data_value) != str:
                    is_matched = False
                    break
                match_compile = re.compile(expect_data_value[2:-2])
                if re.match(match_compile, data_value) is None:
                    is_matched = False
                    break

    assert is_matched, "错误！响应 data：{} 预期 data：{}".format(data, expect_data)

    # 断言 code
    assert result.get("code") == expect.get("result").get("code"),\
        "错误！响应 code：{} 预期 code：{}".format(result.get("code"), expect.get("result").get("code"))
    # 断言 message
    assert result.get("message") == expect.get("result").get("message"), "错误！响应 message：{} 预期 message：{}".format(
        result.get("message"), expect.get("result").get("message"))
