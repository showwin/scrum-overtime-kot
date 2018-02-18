import getpass
import json
import os
import sys

import fire
import requests

CONFIGURATION_MESSAGE = """
To start using sokot, run:

sokot configure
""".strip()
SOKOT_CONFIG_DIR = os.path.join(os.environ['HOME'], '.sokot')
TOKEN_PATH = os.path.join(os.environ['HOME'], '.sokot', 'token')
CONFIG_PATH = os.path.join(os.environ['HOME'], '.sokot', 'config.json')
KOT_API_BASE_URL = 'https://api.kingtime.jp/v1.0'


class SokotConfiguration():
    def _is_configured(self):
        return os.path.exists(TOKEN_PATH) and os.path.exists(CONFIG_PATH)

    def _get_token(self):
        f = open(TOKEN_PATH, 'r')
        return f.read()

    def check(self):
        if self._is_configured():
            return self._get_token()
        print(CONFIGURATION_MESSAGE)
        sys.exit(1)

    def create(self):
        token = getpass.getpass(prompt='Token:')
        if not os.path.exists(SOKOT_CONFIG_DIR):
            os.mkdir(SOKOT_CONFIG_DIR)
        f = open(TOKEN_PATH, 'w')
        f.write(token)
        f.close()
        print("Saved to '{}'\n".format(TOKEN_PATH))

        sprint_length = int(input('Sprint Length (Default: 2):') or 2)
        scrum_start = input('The First Scrum Day (Default: 2018.01.01):') or '2018.01.01'
        config_json = {'sprint_length': sprint_length, 'scrum_start': scrum_start}
        f = open(CONFIG_PATH, 'w')
        f.write(json.dumps(config_json))
        f.close()
        print("Saved to '{}'".format(CONFIG_PATH))


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


class Sokot():
    def __init__(self):
        self._config = SokotConfiguration()
        self._requester = SokotRequester()

    def configure(self):
        self._config.create()
        return 'OK'

    def available(self):
        token = self._config.check()
        resp = self._requester.get('/tokens/{}/available'.format(token), token)
        return resp['available']


def main():
    fire.Fire(Sokot(), name='sokot')


if __name__ == '__main__':
    main()
