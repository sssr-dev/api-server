from typing import Union


class Endpoint:

    name: str = None
    endpoint: str = None
    methods: list = ["GET"]
    version: Union[str, int] = None
    need_auth: bool = False
    db_config: dict = dict()

    def __repr__(self) -> str:
        return f"<Endpoint name='{self.name}' endpoint='{self.endpoint}' methods={self.methods} version='{self.version}' need_auth={self.need_auth} db_config={self.db_config}>"

    def __dict__(self) -> dict:
        return {"rule": self.endpoint, "methods": self.methods}

    def __lshift__(self, mode):
        if mode == "fs":  # fs: Flask settings
            return {"rule": self.endpoint, "methods": self.methods, "endpoint": None}
        return None
