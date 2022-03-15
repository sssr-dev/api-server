from core import Responses, DBHelp, Storage


class GitHubCounter(DBHelp):

    def __init__(self, request):
        super().__init__(Storage.cached_db['git_counter'])

    def do(self):

        return {"some": "text"}, 0
