'''
@说明    :权限接口。
@时间    :2020/2/13 下午4:28:26
@作者    :任秋锴
@版本    :1.0
'''

from .base import base, getToken


class auth(base):
    def __init__(self, token):
        super().__init__(token)

    def list(self, pageNum=1, pageSize=10):
        api_name = "manager/sysuser/list"
        data = {
            "pageNum": pageNum,
            "pageSize": pageSize,
        }
        return self.request(api_name, data)

    def getAllData(self, pageNum=1, pageSize=10):
        while 1:
            response = self.list(pageNum, pageSize)
            rows = response.get("data")
            rows = rows.get("dataList")
            if len(rows) >= pageSize:
                pageNum += 1
                yield rows
            else:
                yield rows
                return

    def create(self, name, specCode):
        api_name = ""
        data = {
            "id": 10270
        }
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

    def updateUserAuth(self, data):
        api_name = "manager/sysuser/update"
        response = self.request(api_name, data, method="POST")
        print(response)
        return self.response(response)

    def updateUserAuthDemo(self, companyId):
        data = {
            "name": "秋锴1",
            "mobile": "13801587423",
            "roleIds": [36], "status2": True, "storeType": 1,
            "companyId": companyId, "companyId2": [],
            "storeId": "", "storeId2": [], "id": 13160, "storeIds": [companyId],
            "status": 1, "type": None, "corpId": None, "isAdmin": 0
        }
        (self.updateUserAuth(data))
