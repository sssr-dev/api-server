import random
import time
from string import ascii_letters, digits

import flask
from flask import abort

from core import Responses, DBHelp, Storage

vk_check_banned = "https://vk.com/away.php?to="


class ShortedLinks(DBHelp):

    def __init__(self, request: flask.Request):
        super().__init__("sqlite", Storage.cached_db['cc'], "links")
        self.args: dict = request.args
        self.from_ip: str = request.headers.get("X-Real-IP") or request.headers.get("Host")

    @staticmethod
    def _create_short():
        return ''.join([random.choice(ascii_letters + digits) for _ in range(5)])

    def _create(self, url: str) -> tuple:
        if not any((url.startswith("http://"), url.startswith("https://"))):
            return {"error": f"Allow only 'http://' or 'https://' urls."}, 10

        url_with_check = vk_check_banned + url
        short = self._create_short()

        url_check = self.sql_get("url_raw", ("url_short", short))
        if url_check:
            while url_check:
                short = self._create_short()
                url_check = self.sql_get("url_raw", ("url_short", short))

        self.sql_insert(("from_ip", "unix_timestamp", "url_raw", "url_check_banned", "url_short"),
                        (self.from_ip, time.time(), url, url_with_check, short))

        return {"short": "https://cc.sssr.dev/" + short, "url": url}, 0

    def _get(self, code):

        url = self.sql_get("url_raw, url_check_banned, counter", ("url_short", code))
        if url:
            url.update({"short": code, "url": url['url_check_banned']})
            del url['url_check_banned']

            self.sql_update(f"counter={url['counter'] + 1}", f"url_short='{code}'")

            data = url, 0
        else:
            data = f"Not found '{code}'", 404

        return data

    def do(self):

        url_create = self.args.get('create')
        short_code = self.args.get("get")

        data = None, 500

        if url_create:
            data = self._create(url_create)

        elif short_code:
            data = self._get(short_code)

        if not data[0]:
            abort(403)

        return Responses.make(Responses.okay(*data) if data[1] == 0 else Responses.error(*data))
