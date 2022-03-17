from core import DBHelp, Storage
from flask import make_response

files = {
    "error": "api/svg_raw/error.svg",
    "magic": "api/svg_raw/magic.svg"
}


class SvgCreator(DBHelp):

    def __init__(self, request):
        super().__init__(Storage.cached_db['svg_creator'])
        self.request = request
        self.default_headers = {
            "Content-Type": "image/svg+xml",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            'Accept': 'application/x-www-form-urlencoded',
            'Access-Control-Allow-Headers': "accept, accept-encoding, content-type, origin, user-agent"
        }

    def make_response(self, data):
        res = make_response(data)
        res.headers.update(self.default_headers)
        res.status_code = 200

        return res

    def get_error_svg(self, error):
        with open(files['error']) as f:
            data = str(f.read()).format(error=error)

        return self.make_response(data)

    def do(self, svg_type: str):

        if svg_type in files.keys():
            path = files[svg_type]
        else:
            return self.get_error_svg("Bad svg.")

        with open(path) as f:
            data = str(f.read())

        username = self.request.args.get('username') or "username?"

        if svg_type == "magic":
            default_width = 200
            default_text_x = 1500

            if len(username) > 14:
                return self.get_error_svg("Too long username")

            else:
                data = data.format(
                    username=username,
                    svg_width=default_width,
                    text_x=default_text_x
                )

        return self.make_response(data)
