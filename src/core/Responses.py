# -*- coding: utf-8 -*-

# Developed by Ahegao Devs
# (c) ahegao.ovh 2022
import flask
from typing import Union, Dict, Any

from flask import Response


class Responses:

    @staticmethod
    def okay(data: dict or int or str or list, code: Union[str, int] = 0) -> Union[Response, dict[str, Union[str, int]]]:
        """
        Стандартизация вывода информации пользователю.

        :param code: Код выполнения
        :param data: Данные для вывода

        :return: {"code": code, "object": data}
        """

        if isinstance(data, Response):
            return data

        return {"code": int(code), "object": data}

    @staticmethod
    def error(error: Union[dict, str], code: Union[str, int]) -> dict:
        """
        Стандартизация вывода ошибки для пользователя.

        :param code:  Код ошибки
        :param error: Error message
        :return: {"code": err.value, "error": err.name}
        """

        if isinstance(error, Response):
            return error

        error = error if isinstance(error, dict) else {"message": f"{error!s}"}
        return {"code": int(code), "error": error}

    @staticmethod
    def make(rv: Union[dict, int, str, list], code: int = 200, cookies: list = None) -> flask.Response:
        """

        :param rv: Данные для вывода
        :param code: Request code
        :param cookies: Отправляемые куки
        :return: Response
        """

        if isinstance(rv, Response):
            return rv

        if cookies is None:
            cookies = []
        resp = flask.jsonify(rv)
        resp.headers.update({
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            'Accept': 'application/x-www-form-urlencoded',
            'Access-Control-Allow-Headers': "accept, accept-encoding, content-type, origin, user-agent"
        })
        for cookie in cookies:
            resp.set_cookie(cookie)
        resp.status_code = code
        return resp
