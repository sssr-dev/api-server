from flask import request
from core import InitAPI, Responses
import api

codes = (403, 404, 500)
iapp = InitAPI("config.json")
endpoints = iapp.endpoints
app = iapp.app


@app.route('/')
def pa():
    j = dict()
    for k, v in endpoints.items():
        j.update({k: f'{v!r}'})
    return Responses.okay(j)


iapp.app_errors_handler(codes, lambda error: (Responses.error(error.name, error.code), error.code))

iapp.add_route("cc", lambda: api.ShortedLinks(request).do())

if __name__ == '__main__':
    iapp.run()
