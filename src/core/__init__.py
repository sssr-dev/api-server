import flask

from .init_system import InitAPI, Storage
from .Responses import Responses
from .DBHelp import DBHelp
from .Endpoint import Endpoint


class ProxyHeaders:
    NGINX_IP = "Ng-Real-Ip"
    NGINX_HOSTNAME = "Ng-Real-Hostname"

    CLOUDFLARE_IP = "Cf-Connecting-Ip"


def get_hostname(request: flask.Request):
    headers = request.headers
    hostname = None

    if headers.get('Cdn-Loop') == "cloudflare":
        # Cloudflare proxy
        from_ip: str = headers.get(ProxyHeaders.CLOUDFLARE_IP)
    else:
        # Nginx proxy
        from_ip: str = headers.get(ProxyHeaders.NGINX_IP)
        # Add to nginx: proxy_set_header Ng-Real-Hostname $host;
        hostname = headers.get(ProxyHeaders.NGINX_HOSTNAME)

    if from_ip is None:
        # if no proxy
        from_ip: str = request.headers.get("Host")

    if hostname is None:
        hostname = request.host

    return from_ip, hostname
