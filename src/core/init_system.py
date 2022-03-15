import json
import os
from typing import Union, Any, Callable
import sqlite3
from loguru import logger
from flask import Flask

from .Responses import Responses
from .Endpoint import Endpoint
from .Storage import Storage

Storage = Storage()


class InitAPI:

    # noinspection PyTypeChecker
    def __init__(self, config_path):

        self.log = logger
        self.debug = self.log.debug

        self.name: str = None

        self.__flask: Flask = None
        self.flask_settings: dict = None

        self.endpoints: dict = dict()
        self.endpoints_info: dict = None

        self.config_path = config_path

        self._read_config()
        self._create_endpoints()

        self._cached_db: dict = dict()

    def _read_config(self):
        self.debug("_read_config(self)")
        if os.path.isfile(self.config_path):
            self.debug(f"Config file: %s - found" % self.config_path)
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        else:
            self.debug(f"Cannot found config file at %s. Use default." % self.config_path)
            config = {"name": "NO NAME", "flask_settings": {"host": "localhost", "port": 3000}}
            self.debug(config)

        self.name = config.get("name")
        self.flask_settings = config.get("flask_settings")
        self.endpoints_info = config.get("endpoints_info")

    def _create_endpoints(self):
        for k, v in self.endpoints_info.items():
            e = Endpoint()
            e.import_name = k
            e.name = v.get("name")
            e.methods = v.get("methods") or ['GET']
            e.endpoint = v.get('endpoint')
            e.version = v.get("version")
            e.need_auth = v.get("need_auth")
            e.db_config = v.get("db_config")
            self.debug(f"{e!r}")
            self.endpoints.update({k: e})

    def app_errors_handler(self, codes: Union[list, tuple, int], f: Any):
        if isinstance(codes, int):
            codes = (codes, )

        for code in codes:
            self.debug(f"self.app.register_error_handler({code}, {f})")
            self.app.register_error_handler(code, f)

    def get_db_conn(self, endpoint: str):

        if self._cached_db.get(endpoint):
            if self.endpoints[endpoint].db_config['type'] != "sqlite":
                return self._cached_db[endpoint]

        db_config = self.endpoints[endpoint].db_config
        db_type = db_config.get('type').lower()

        if db_type == "sqlite":
            db_path = db_config['path']

            if os.path.isfile(db_path):
                db_conn = sqlite3.connect(db_path)
                self._cached_db.update({endpoint: {"raw": db_config, "conn": db_path}})
                Storage.cached_db.update({endpoint: {"raw": db_config, "conn": db_path}})
                return db_conn

            else:
                raise ValueError(f"Cannot find '{db_path}'")

        raise ValueError(f"What is '{db_type}'?")

    def response(self, data):

        return Responses.make(Responses.okay(*data) if data[1] == 0 else Responses.error(*data), 404 if data[1] == 404 else 200)

    def add_route(self, endpoint: str, f: Callable):
        self.debug(f"Add route for endpoint '{endpoint}'")
        self.get_db_conn(endpoint)
        endpoint = self.endpoints[endpoint]
        self.debug(endpoint)
        l = lambda *args, **kwargs: self.response(f(*args, **kwargs))
        l.__name__ = endpoint.import_name
        self.app.route(**endpoint << "fs")(l)

    @property
    def app(self) -> Flask:
        if self.__flask is None:
            self.__flask = Flask(import_name=self.name)
        return self.__flask

    def run(self):
        self.__flask.run(**self.flask_settings)
