import requests
import logging

class MytAPI:
    """
    MYT设备API接口类
    提供设备查询相关功能
    """
    baseurl = "http://127.0.0.1:5000"  # 启动 SDK 后实际可用的地址

    @classmethod
    def set_baseurl(cls, url):
        """
        动态设置 baseurl
        """
        cls.baseurl = url

    @classmethod
    def query_myt(cls):
        """
        查询局域网内设备信息（通过本地 SDK 服务）

        返回格式:
        {
            "code": 200,
            "message": "success",
            "data": {
                "192.168.x.x": "设备码",
                ...
            }
        }
        """
        try:
            response = requests.get(f"{cls.baseurl}/host_api/v1/query_myt", timeout=3)
            response.raise_for_status()  # 如果响应非200，将引发异常
            json_data = response.json()

            # 校验返回结构
            if "code" in json_data and "data" in json_data:
                return json_data
            else:
                return {
                    "code": 500,
                    "message": "返回数据格式错误",
                    "data": {}
                }

        except requests.exceptions.RequestException as e:
            logging.warning(f"[MytAPI] 查询设备失败: {e}")
            # 可返回示例数据作为降级处理
            return {
                "code": 503,
                "message": "无法连接设备服务，返回模拟数据",
                "data": {
                    "192.168.181.27": "e5ef14d8cee888ae8a5e511d79d71593d",
                    "192.168.181.28": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
                }
            }

    @classmethod
    def login(cls, user, password):
        try:
            response = requests.get(f"{cls.baseurl}/login/{user}/{password}", timeout=3)
            response.raise_for_status()
            json_data = response.json()

            # 标准化返回结构
            if json_data.get("code") == 200 and isinstance(json_data.get("msg"), str):
                return {
                    "code": 200,
                    "message": "success",
                    "data": json_data["msg"]
                }
            else:
                return {
                    "code": 500,
                    "message": "登录失败，返回格式错误",
                    "data": {}
                }
        except requests.exceptions.RequestException as e:
            logging.warning(f"[MytAPI] 登录失败: {e}")
            return {
                "code": 500,
                "message": "请求异常",
                "data": {}
            }
