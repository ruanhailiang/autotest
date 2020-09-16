from config import host
import requests
from tools.get_log import GetLog

log = GetLog.get_logger()


class Api(object):
    # 1. 初始化
    def __init__(self, case):
        # 1. 提取 url = host+path
        self.url = case.get("protocol") + "://" + host + case.get("path")
        # 2. 请求方法
        self.method = case.get("method")
        # 3. 请求参数类型
        self.param_type = case.get("param_type")
        # 4. 请求信息头
        self.headers = case.get("headers")
        # 5. 请求参数
        self.params = case.get("params")

    # 2. 查询方法
    def _get(self):
        log.info("正在调用 get请求方法")
        return requests.get(url=self.url, params=self.params, headers=self.headers)

    # 3. 新增方法
    def _post(self):
        log.info("正在调用 post请求方法")
        # 判断参数类型[json\data]
        if self.param_type == "json":
            return requests.post(url=self.url, json=self.params, headers=self.headers)
        elif self.param_type == "data":
            return requests.post(url=self.url, data=self.params, headers=self.headers)
        elif self.param_type == "params":
            return requests.post(url=self.url, params=self.params, headers=self.headers)

    # 4. 更新方法-put
    def _put(self):
        log.info("正在调用put请求方法")
        return requests.put(url=self.url, data=self.params, json=self.params, headers=self.headers)

    # 5. 更新方法-patch
    def _patch(self):
        log.info("正在调用put请求方法")
        return requests.patch(url=self.url, json=self.params, headers=self.headers)


    # 6. 删除方法
    def _delete(self):
        log.info("正在调用delete请求方法")
        return requests.delete(url=self.url, params=self.params, data=self.params, headers=self.headers)

    # 7. Head方法
    def _head(self):
        log.info("正在调用head请求方法")
        return requests.head(url=self.url, params=self.params, data=self.params, headers=self.headers)

    # 8. options方法
    def _options(self):
        log.info("正在调用options请求方法")
        return requests.options(url=self.url, params=self.params, data=self.params, headers=self.headers)

    # . 调用运行方法
    def run_method(self):
        log.info("正在调用运行接口方法")
        # 判断方法
        if self.method == "get":
            return self._get()
        elif self.method == "post":
            return self._post()
        elif self.method == "put":
            return self._put()
        elif self.method == "delete":
            return self._delete()
        elif self.method == "head":
            return self._head()
        elif self.method == "options":
            return self._options()
        elif self.method == "patch":
            return self._patch()