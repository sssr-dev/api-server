from core import DBHelp, Storage
from flask import make_response, request

svg_path = "api/svg_raw"

styles = {
    "flat": {"svg_style": '<mask id="id_1"><rect width="%(width)s" height="%(height)s" rx="0" fill="#fff"/></mask>',
             "g_1": 'mask="url(#id_1)"'},
    "for-the-badge": {"svg_style": "", "g_1": 'shape-rendering="crispEdges"'},
}

files = {
    "default": f"{svg_path}/default.svg",
    "error": f"{svg_path}/error.svg",
    "magic": f"{svg_path}/magic_ico.svg",
}


class SvgCreator(DBHelp):

    def __init__(self):
        super().__init__(Storage.cached_db['svg_creator'])
        self.style = {"svg_style": "", "g_1": ""}
        self.svg_params = {}
        self.request = request
        self.default_headers = {
            "Content-Type": "image/svg+xml",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            'Accept': 'application/x-www-form-urlencoded',
            'Access-Control-Allow-Headers': "accept, accept-encoding, content-type, origin, user-agent"
        }

    def make_response(self, data, code=200):
        res = make_response(data)
        res.headers.update(self.default_headers)
        res.status_code = code

        return res

    def get_error_svg(self, error):
        with open(files['error']) as f:
            data = str(f.read()).format(error=error)

        return self.make_response(data, 500)

    def get_svg_settings(self):
        get_arg = self.request.args.get
        add_rect = ""

        width = get_arg("width") or 100
        height = get_arg("height") or 28
        color = get_arg('color') or "#fe7d37"
        font_size = get_arg('font_size') or 11

        svg_color = get_arg('svg_color')

        if svg_color:
            add_rect += f'<rect width="{width}" height="{height}" fill="{svg_color}"/>\n'

        text_position_x_1 = width / 2

        text_y = (height / 2) + (font_size / 2) - 1

        settings = {

            "title": "title",

            "svg_style": None,
            "g_1": None,

            "svg_width": width,
            "svg_height": height,
            "color": color,
            "rect_width_1": width,
            "rect_width_2": 1,

            "add_rect": add_rect,

            "text_position_x_1": text_position_x_1,
            "text_position_x_2": 0,
            "text_position_y_1": text_y,
            "text_position_y_2": text_y,

            "text_font_size_1": font_size,
            "text_font_size_2": font_size,

            "pre_text": "",

            "text_string_1": "{text_string_1}",
            "text_string_2": "{text_string_2}"
        }

        self.style['svg_style'] %= {'width': width, 'height': height}

        settings.update(self.style)
        self.svg_params = settings

        return self.svg_params

    def set_g2_center(self, obj):
        g2 = len(obj) * (self.svg_params['text_font_size_2'] - 0.5)

        self.svg_params['text_position_x_2'] = g2 / 2 + self.svg_params["svg_width"]

        self.svg_params["svg_width"] += g2
        self.svg_params["rect_width_2"] = self.svg_params["svg_width"] - self.svg_params["rect_width_2"]

    def do(self, svg_type: str):

        get_arg = self.request.args.get
        style = get_arg("style") or "for-the-badge"
        self.get_svg_settings()

        if style in styles.keys():
            self.style = styles[style]
        else:
            return self.get_error_svg("Unknown style")

        with open(files['default']) as f:
            data = f.read()

        if svg_type in ("magic", ):
            username = get_arg('username').replace("+", " ") if get_arg('username') else "Username?"

            with open(files[svg_type]) as f:
                ico = f.read()

            self.svg_params['text_position_x_1'] += 10
            self.svg_params['pre_text'] = ico.format(
                x=3,
                y=4,
                view_box="0 0 512 512",
                height=20,
                width=20
            )

            self.svg_params["title"] = "MAGIC"
            self.svg_params['text_string_1'] = "MAGIC BY"
            self.svg_params['text_string_2'] = username
            self.set_g2_center(username)

        else:
            return self.get_error_svg("Unknown svg_type")

        return self.make_response(data.format(**self.svg_params))
