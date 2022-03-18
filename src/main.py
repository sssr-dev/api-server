from flask import request
import requests

from core import InitAPI, Responses
import core.tools
import api

codes = (403, 404, 405, 500)
iapp = InitAPI("config.json")
endpoints = iapp.endpoints
app = iapp.app
storage = iapp.storage


def set_self_ip(first=True):
    if storage.self_ip is not None:
        print(f"set_self_ip: {storage.self_ip=}")
        return
    if first:
        import threading
        t = threading.Thread(target=set_self_ip, args=(False, ))
        print("set_self_ip: Start thread.")
        t.start()
        del threading
    else:
        from time import sleep
        print("set_self_ip: Sleep for 3 sec.")
        sleep(3)
        r = requests.get("https://api-dev.sssr.dev/error/").json()
        if r.get("error"):
            self_ip = r['error']['ip']
            storage.self_ip = self_ip
            print(f"{self_ip=}")
        else:
            print(f"error: {r}")
        del sleep


@app.route('/')
def pa():
    from_ip, hostname = core.tools.get_hostname(request)

    j = dict()
    j.update(
        {
            "api_info": {
                "name": iapp.name,
                "version": iapp.config['version'],
                "build": iapp.config['build'],
                "debug": iapp.config['flask_settings']['debug'],
            },
            "connection_info": {
                "hostname": hostname,
                "ip": from_ip
            },
            "endpoints": {

            }
        }
    )
    for k, v in endpoints.items():
        j['endpoints'].update({k: f'{v!s}'})

    return Responses.okay(j)


iapp.app_errors_handler(codes, lambda error: (Responses.make(Responses.error(error.name, error.code)), error.code))

iapp.add_route("cc", lambda: api.ShortedLinks())
iapp.add_route("svg_creator", lambda: api.SvgCreator())
iapp.add_route("auth", lambda: api.SSSRAuth())

if __name__ == '__main__':
    set_self_ip()
    iapp.run()
