from urllib.parse import urlparse

from flask import request
from core import InitAPI, Responses, get_hostname
import api


codes = (403, 404, 405, 500)
iapp = InitAPI("config.json")
endpoints = iapp.endpoints
app = iapp.app


@app.route('/')
def pa():
    from_ip, hostname = get_hostname(request)

    j = dict()
    j.update({"name": iapp.name,
              "version": iapp.config['version'],
              "client_info": {
                  "ip": from_ip,
                  "hostname": hostname
              },
              "endpoints": {}})
    for k, v in endpoints.items():
        j['endpoints'].update({k: f'{v!s}'})

    return Responses.okay(j)


iapp.app_errors_handler(codes, lambda error: (Responses.make(Responses.error(error.name, error.code)), error.code))

iapp.add_route("cc", lambda: api.ShortedLinks(request))
iapp.add_route("git_counter", lambda: api.GitHubCounter(request))
iapp.add_route("auth", lambda: api.SSSRAuth(request))

if __name__ == '__main__':
    iapp.run()
