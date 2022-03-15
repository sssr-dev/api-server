import random
import time
import urllib.parse
from string import ascii_letters, digits

import flask
from flask import abort, redirect

from core import DBHelp, Storage, get_hostname

vk_check_banned = "https://vk.com/away.php?utf=1&to="


class ShortedLinks(DBHelp):

    def __init__(self, request: flask.Request):
        super().__init__(Storage.cached_db['cc'])
        self.args: dict = request.args
        self.form: dict = request.form
        self.from_ip, self.hostname = get_hostname(request)

        self.short_code_len = 5

    def _create_short(self):
        return ''.join([random.choice(ascii_letters + digits) for _ in range(self.short_code_len)])

    def _create(self, url: str) -> tuple:
        if not any((url.startswith("http://"), url.startswith("https://"))):
            return {"error": f"Allow only 'http://' or 'https://' urls."}, 10

        url_with_check = vk_check_banned + urllib.parse.quote_plus(url)
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
            data = {"message": f"No url for '{code}'."}, 404

        return data

    def _nginx_cc(self):
        short_code = self.args.get('nginx')

        if len(short_code) == self.short_code_len:
            url_object, exit_code = self._get(short_code)
            if exit_code == 0:
                return redirect(url_object['url'], 307)

        return '<script>history.back(-1)</script>'

    def do(self):

        if self.hostname == "cc.sssr.dev":
            return self._nginx_cc()

        ver = self.args.get("v") or 10  # 1.1
        last_ver = "1.1"
        available_vers = ['1.0', '1.1']
        deprecation_warn_example = \
            f"Deprecated warn: 'cc' version {{}} has deprecated warn on fields: {{}}. Use {last_ver} 'cc' version."

        if isinstance(ver, str):
            ver = ver.replace(".", '')
            if ver.isdigit():
                ver = int(ver)

        if ver == 10:
            deprecation_warn = True
            fields = ['create', 'get']
            deprecation_warn_message = deprecation_warn_example.format("1.0", ", ".join(field for field in fields))
            fields_error_message = "'create' for create cc url or 'get' get url from code"
            url_create = self.args.get("create")  # GET field 'create'
            short_code = self.args.get("get")  # GET field 'get'

        elif ver == 11:
            deprecation_warn = False
            fields = ['url']
            deprecation_warn_message = None
            fields_error_message = "POST field 'url' for create cc or GET field 'code' for get raw url"
            url_create = self.form.get('url')  # POST field 'url'
            short_code = self.args.get("code")  # GET field 'url'

        else:
            return {"message": f"Invalid field '{ver}'. Available versions: {', '.join(ver for ver in available_vers)}"}, 11

        if url_create:
            data = self._create(url_create)

        elif short_code:

            if len(short_code) != self.short_code_len:
                data = {"message": "Invalid code"}, 404

            else:
                data = self._get(short_code)

        else:
            data = {"message": f"Missed one of fields: {fields_error_message}"}, 12

        if not data[0]:
            abort(403)

        if deprecation_warn:
            data[0].update({"warn": deprecation_warn_message})

        return data
