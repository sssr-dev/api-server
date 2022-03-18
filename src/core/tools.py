from urllib.parse import urlparse

import flask


class ProxyHeaders:
    NGINX_IP = r"Ng-Real-Ip"
    NGINX_HOSTNAME = r"Ng-Real-Hostname"

    CLOUDFLARE_IP = r"Cf-Connecting-Ip"


def get_hostname(request: flask.Request):
    headers = request.headers

    if headers.get('Cdn-Loop') == "cloudflare":
        # Cloudflare proxy
        from_ip: str = headers.get(ProxyHeaders.CLOUDFLARE_IP)
    else:
        # Nginx proxy
        from_ip: str = headers.get(ProxyHeaders.NGINX_IP)

    if from_ip is None:
        # if no proxy
        from_ip: str = request.headers.get("Host")

    # Add to nginx: proxy_set_header Ng-Real-Hostname $host;
    hostname: str = headers.get(ProxyHeaders.NGINX_HOSTNAME)
    if hostname is None:
        hostname = urlparse(request.base_url).hostname

    return from_ip, hostname
