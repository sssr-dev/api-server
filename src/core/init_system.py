import json
import logging
import os
from typing import Union, Any, Callable, List
import sqlite3
from urllib.parse import quote_plus

from loguru import logger
from flask import Flask, redirect

from .Responses import Responses
from .Endpoint import Endpoint
from .Storage import Storage as _storage

Storage = _storage()


def fake_log(*x):

    phrase = (x[2] % x[3:][0]) if len(x[3:][0]) > 0 else x[2]

    if "\n" in phrase:
        phrase = "\n" + phrase
    logger.info(phrase)


class InitSystem:

    # noinspection PyTypeChecker
    def __init__(self, config_path):

        logging.Logger._log = fake_log

        self.storage = Storage

        self.log = logger
        self.debug = self.log.debug

        self.config = {"name": "NO NAME", "flask_settings": {"host": "localhost", "port": 3000}}

        self.name: str = None
        self.base_site = None

        self.__flask: Flask = None
        self.flask_settings: dict = None

        self.endpoints: dict = {}
        self.redirects: List[dict] = []

        self.endpoints_config: dict = {}
        self.redirects_config: dict = {}

        self.config_path = config_path

        self._read_config()
        self._create_endpoints()
        self._create_redirects()

        self._cached_db: dict = dict()

    def _read_config(self):
        self.debug("_read_config(self)")
        if os.path.isfile(self.config_path):
            self.debug(f"Config file: %s - found" % self.config_path)
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.debug(f"Cannot found config file at %s. Use default." % self.config_path)
            self.debug(self.config)

        self.name = self.config.get("name")
        self.base_site = self.config.get("base_site")
        self.flask_settings = self.config.get("flask_settings")
        self.endpoints_config = self.config.get("endpoints")
        self.redirects_config = self.config.get("redirects")

    def _create_endpoints(self):
        for k, v in self.endpoints_config.items():
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

    def _create_redirects(self):
        for v in self.redirects_config.values():
            from_route = v['from']
            ref = ""
            if v['ref']:
                ref += quote_plus(v['ref'])
            l = lambda *x: redirect(v['to'].format(base_site=self.base_site)+ref, v['code'])
            l.__name__ = from_route

            self.app.route(from_route)(l)
            self.debug(f"Add redirect '{from_route}' to '{v['to'].format(base_site=self.base_site)+ref}' with code {v['code']}")
            self.redirects.append(v)

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

    @staticmethod
    def response(data):
        if isinstance(data, tuple) and len(data) == 2:
            return Responses.make(Responses.okay(*data) if data[1] == 0 else Responses.error(*data), 404 if data[1] == 404 else 200)
        return data

    def add_route(self, endpoint: str, cls: Callable):
        self.debug(f"Add route for endpoint '{endpoint}'")
        self.get_db_conn(endpoint)
        endpoint = self.endpoints[endpoint]
        self.debug(endpoint)
        l = lambda *args, **kwargs: self.response(cls().do(*args, **kwargs))
        l.__name__ = endpoint.import_name
        self.app.route(**endpoint << "fs")(l)

    @property
    def app(self) -> Flask:
        if self.__flask is None:
            self.__flask = Flask(import_name=self.name)
        return self.__flask

    def run(self):

        if os.getenv("FLASK_DEBUG"):
            self.flask_settings['debug'] = True

        self.__flask.run(**self.flask_settings)
