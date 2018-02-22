import getpass
import json
import os

import requests
import requests.auth

PROXY_PATH = os.path.join(os.environ['HOME'], '.sokot', 'proxy')

class SokotProxy():
    def _set_proxy(self, server, port, user, password):
        proxy = 'http://{}:{}@{}:{}/'.format(user, password, server, port)
        proxy_conf = {'http': proxy, 'https': proxy}
        f = open(PROXY_PATH, 'w')
        f.write(json.dumps(proxy_conf))
        f.close()

    def configure(self):
        server = input('Server (e.g. example.com):')
        port = input('Port:')
        user = input('User:')
        password = getpass.getpass(prompt='Password:')

        if server and port:
            self._set_proxy(server, port, user, password)
        print("Saved to '{}'\n".format(PROXY_PATH))

    def delete(self):
        if os.path.exists(PROXY_PATH):
            os.remove(PROXY_PATH)

    def _get(self):
        """
        コマンドのインターフェイスには出さないが、他のモジュールからは呼ばれる
        """
        if not os.path.exists(PROXY_PATH):
            return {}
        f = open(PROXY_PATH, 'r')
        json_str = f.read()
        f.close()
        return json.loads(json_str)
