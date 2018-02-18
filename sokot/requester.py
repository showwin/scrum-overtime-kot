import json

import requests

KOT_API_BASE_URL = 'https://api.kingtime.jp/v1.0'


class SokotRequester():
    def __init__(self):
        self.base_url = KOT_API_BASE_URL
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer {token}'
        }

    def get(self, uri, token):
        self.headers['Authorization'] = self.headers['Authorization'].format(token=token)
        url = self.base_url + uri
        resp = requests.get(url, headers=self.headers)
        return json.loads(resp.text)

    def post(self, uri, token, payload):
        self.headers['Authorization'] = self.headers['Authorization'].format(token=token)
        url = self.base_url + uri
        resp = requests.post(url, headers=self.headers, data=payload)
        return json.loads(resp.text)
