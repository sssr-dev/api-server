from flask import request
from core import InitAPI, Responses
import api

codes = (403, 404, 500)
iapp = InitAPI("config.json")
endpoints = iapp.endpoints
app = iapp.app


@app.route('/')
def pa():
    headers = request.headers
    hostname = request.host

    if headers.get('Cdn-Loop') == "cloudflare":
        # Cloudflare proxy
        from_ip: str = request.headers.get("Cf-Connecting-Ip")
    else:
        # Nginx proxy
        from_ip: str = request.headers.get("X-Real-IP")
        # Add to nginx: proxy_set_header X-Real-HostName $host;
        hostname = headers.get('X-Real-Hostname') or hostname

    if from_ip is None:
        # if no proxy
        from_ip: str = request.headers.get("Host")

    j = dict()
    j.update({"name": iapp.name, "version": iapp.config['version'], "client_info": {"ip": from_ip, "href": hostname}, "endpoints": {}})
    for k, v in endpoints.items():
        j['endpoints'].update({k: f'{v!s}'})

    return Responses.okay(j)


iapp.app_errors_handler(codes, lambda error: (Responses.make(Responses.error(error.name, error.code)), error.code))

iapp.add_route("cc", lambda: api.ShortedLinks(request).do())
iapp.add_route("git_counter", lambda: api.GitHubCounter(request).do())

if __name__ == '__main__':
    iapp.run()
