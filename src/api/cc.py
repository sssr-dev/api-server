from flask import abort

from core import Responses, DBHelp, Storage

vk_check_banned = "https://vk.com/away.php?to="


class ShortedLinks(DBHelp):

    def __init__(self, args):
        super().__init__("sqlite", Storage.cached_db['cc'], "links")
        self.args: dict = args

    def _create(self, url: str) -> tuple:
        if not any((url.startswith("http://"), url.startswith("https://"))):
            return {"error": f"Allow only 'http://' or 'https://' urls."}, 10

        return {"create": vk_check_banned + url}, 0

    def do(self):

        url_to = self.args.get('to')
        url_create = self.args.get('create')
        url_raw = self.args.get("raw")

        data = None, 500

        if url_to:
            data = {"from": url_to}, 0

        elif url_create:
            data = self._create(url_create)

        elif url_raw:
            data = {"url_raw": self.sql_get("url_raw", ("url_short", url_raw)).get("url_raw")}, 0

        if not data:
            abort(403)

        return Responses.make(Responses.okay(*data) if data[1] == 0 else Responses.error(*data))
