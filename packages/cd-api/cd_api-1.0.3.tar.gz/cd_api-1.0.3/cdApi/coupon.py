'''
@说明    :优惠券接口。
@时间    :2020/3/19 下午4:51:48
@作者    :任秋锴
@版本    :1.0
'''

from .base import base, getToken


class coupon(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, pageNum=1, pageSize=10):
        api_name = "manager/live_room/list"
        data = {
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        return self.request(api_name, data)

    def sync(self, order_code):
        api_name = "manager/order/order_invoice"
        data = {"orderCodes": order_code}
        return self.request(api_name, data, method="POST")

    def create(self, data):
        api_name = ""
        return self.request(api_name, data, method="POST")

    def read(self, _id):
        api_name = "manager/coupon/info"
        data = {
            "id": _id,
        }
        response = self.request(api_name, data, method="GET")
        # print(response)
        return self.response(response)

    def update(self, data):
        api_name = "manager/coupon/edit"
        response = self.request(api_name, data, method="POST")
        print(response)
        # return self.response(response)

    def updateDemo(self):
        data = {
            "id": 230,
            "storeList": [
                {"id": 1290, "type": 0, "parentId": 1289}
            ],
        }
        return self.update(data)


    def delete(self):
        pass

