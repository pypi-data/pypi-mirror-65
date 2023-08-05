import requests
from json import loads, dumps

HEADERS = {
    'User-Agent': 'Python Var Client'
}


class Var:
    def __init__(self, var_name):
        self.url = "http://api.wonderbits.cn/var"
        self.var_name = var_name    # instance variable unique to each instance

    def update(self, value):

        resp = requests.post(self.url, json={
            'name': self.var_name, 'value': value}, headers=HEADERS)
        print(resp.request.headers)

    def get(self, rank=1):
        response = requests.get(
            self.url, {"name": self.var_name, "index": rank-1})
        res = response.json()
        if res["code"] == 0:
            return loads(res["data"])
        else:
            return res["msg"]

    def history(self, page=1, per_page=20):
        response = requests.get(
            self.url + "/history", {"name": self.var_name, "page": page, "perPage": per_page})
        res = response.json()
        if res["code"] == 0:
            if len(res["data"]) == 0:
                return []
            return res["data"]
        else:
            return res["msg"]

    def __repr__(self):
        return str(self.get())


if __name__ == "__main__":
    i = Var('test')
    i.update(12346)
    print(i.get())
    print(i.history())
