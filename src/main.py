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


iapp.get_db_conn('cc')
app.add_url_rule(**endpoints['cc'] << "fs", f=lambda: api.ShortedLinks(request.args))

if __name__ == '__main__':
    iapp.app_errors_handler(codes, lambda error: Responses.error(error.name, error.code))
    # Responses.error("Allow only 'http://' or 'https://' urls.", 10)
    iapp.run()
