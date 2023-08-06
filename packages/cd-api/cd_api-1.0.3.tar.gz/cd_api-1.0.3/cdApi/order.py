'''
@说明    :订单接口。
@时间    :2020/3/19 下午4:51:48
@作者    :任秋锴
@版本    :1.0
'''

from .base import base


class order(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, pageNum=1, pageSize=10):
        api_name = "manager/store/get_sysuser_store_tree"
        data = {
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        return self.request(api_name, data)

    def sync(self, order_code):
        # 向客户同步销售订单 
        api_name = "manager/order/order_invoice"
        data = {"orderCodes": order_code}
        return self.request(api_name, data, method="POST")

    def syncReturn(self, order_code, type=None):
        # 向客户同步售后订单
        api_name = "manager/order/order_invoice"
        data = {"returnCodes": order_code}
        if type:
            data["type"] = type
        return self.request(api_name, data, method="POST")

    def create(self, data):
        api_name = ""
        return self.request(api_name, data, method="POST")

    def read(self, _id):
        api_name = "manager/store/info"
        data = {
            "id": _id,
        }
        response = self.request(api_name, data, method="GET")
        # print(response)
        return response

    def update(self, data):
        api_name = "manager/store/update"
        response = self.request(api_name, data, method="POST")
        # print(response)
        return self.response(response)

    def updateDemo(self):
        data = {
            'logoUrl': "",
            'storeCode': "",
            'storeType': 0,
            'address': "上海市浦东新区浦东南路2250号",
            'province': "上海市",
            'city': "上海市",
            'area': "浦东新区",
            'longitude': "123.51",
            'latitude': "31.20",
            'level': 2,
            'managerMobile': "",
            'managerName': "",
            'name': "测试店（滨江）",
            'parentId': 10269,
            'type': 0,
            'takeStatus': 0,
            'accountId': None,
            'regionValue': ["上海市", "上海市", "浦东新区"],
        }
        _id = 10270
        self.update(_id, data)

    def updateGPS(self, _id, lat, lng):
        data = self.read(_id)
        data = data.get("data")
        data["longitude"] = lng
        data["latitude"] = lat
        self.update(data)

    def delete(self):
        pass
