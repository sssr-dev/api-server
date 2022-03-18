from core import DBHelp, Storage


class SSSRAuth(DBHelp):

    def __init__(self):
        super().__init__(Storage.cached_db['auth'])

    def do(self, method: str = None):

        return {"method": method}, 0
