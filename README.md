# api server

<p align="center">
    <a href="https://github.com/sssr-dev/api-server/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/sssr-dev/api-server?style=for-the-badge"></a>    
    <a href="https://github.com/sssr-dev/api-server/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/sssr-dev/api-server?style=for-the-badge"></a>    
    <a href="https://github.com/SantaSpeen"><img src="./.readme_files/magic_logo.svg" alt="magic"></a>
    <br/>
    <a href="./src/main.py">
        <img src="./.readme_files/preview.png" alt="preview ds">
    </a>
    <br/>
</p>

### Start

```shell
# Shell

$ git clone https://github.com/sssr-dev/api-server.git
  # Cloning repo
$ cd src
$ pip install -r requirements.txt
  # Install all dependents
$ python main.py
  # Start develop server
  
```

### Nginx configuration
```js
server {
    server_name sssr.dev www.sssr.dev;
    listen 80;
    listen 443;
    listen [::]:80;
    listen [::]:443;


    error_page 404 /;

    location / {
        root /var/www/sssr.dev;
        index index.html;
    }
}

server {
    server_name api.sssr.dev;
    listen 80;
    listen 443;
    listen [::]:80;
    listen [::]:443;

    location / {
        proxy_pass http://127.0.0.1:11491/;
        proxy_set_header Ng-Real-Ip $remote_addr;
        proxy_set_header Ng-Real-Hostname $host;    
    }
}
server {
    
    server_name cc.sssr.dev;
    listen 80;
    listen 443;
    listen [::]:80;
    listen [::]:443;
    
    location / {
        proxy_pass http://127.0.0.1:11491/cc?nginx=;   
        proxy_set_header Ng-Real-Ip $remote_addr;
        proxy_set_header Ng-Real-Hostname $host;  
    }
}
```