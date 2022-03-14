import json
import os
from typing import Union, List

from loguru import logger

from flask import Flask


class Endpoint:

    name: str = None
    endpoint: str = None
    version: Union[str, int] = None
    need_auth: bool = False
    db_config: dict = dict()

    def __repr__(self) -> str:
        return f"<Endpoint name={self.name} endpoint={self.endpoint} version={self.version} need_auth={self.need_auth} db_config={self.db_config}>"


class InitAPI:

    # noinspection PyTypeChecker
    def __init__(self, config_path):

        self.log = logger
        self.debug = self.log.debug

        self.name: str = None

        self.__flask: Flask = None
        self.flask_settings: dict = None

        self.endpoints: List[Endpoint] = list()
        self.endpoints_info: dict = None

        self.config_path = config_path

        self._read_config()
        self._create_endpoints()

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
            e.name = k
            e.endpoint = v.get('endpoint')
            e.version = v.get("version")
            e.need_auth = v.get("need_auth")
            e.db_config = v.get("db_config")
            self.debug(f"{e!r}")
            self.endpoints.append(e)

    @property
    def flask(self):
        if self.__flask is None:
            self.__flask = Flask(import_name=self.name)
        return self.__flask
