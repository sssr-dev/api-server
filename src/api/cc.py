from flask import abort

from core import Responses, DBHelp, Storage

vk_check_banned = "https://vk.com/away.php?to="


class ShortedLinks(DBHelp):

    def __init__(self, args):
        super().__init__("sqlite", Storage.cached_db['cc'])
        self.args: dict = args

    def _create(self, url: str) -> dict:
        if not any((url.startswith("http://"), url.startswith("https://"))):
            return Responses.error(f"Allow only 'http://' or 'https://' urls.", 10)

        return Responses.okay({"create": vk_check_banned + url})

    def do(self):

        url_to = self.args.get('to')
        url_create = self.args.get('create')
        url_raw = self.args.get("raw")

        data = None

        if url_to:
            data = Responses.okay({"from": url_to})

        elif url_create:
            return self._create(url_create)

        elif url_raw:
            return {"raw": url_raw}

        if not data:
            abort(403)

        return data
