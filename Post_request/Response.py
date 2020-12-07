import requests
import json


class MerchantPost:
    response = None
    data = {}
    token = None
    response_content = None

    def post(self, url):
        self.response = requests.post(url, data=self.data, timeout=120)

    def response2json(self):
        self.response_content = self.response.json()
        # print(self.response_content)

    def response2html(self):
        self.response_content = json.loads(self.response.content)




