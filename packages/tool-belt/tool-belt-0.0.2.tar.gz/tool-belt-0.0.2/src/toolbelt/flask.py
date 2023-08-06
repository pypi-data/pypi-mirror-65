from dataclasses import dataclass

from flask import Flask
from flask.views import View


@dataclass
class Path(object):
    endpoint_name: str
    base_url: str
    pk_name: str = "id"
    pk_type: str = "int"


def register_rest_api(app: Flask, view_cls: View, path: Path, *view_args, **view_kwargs):
    view_func = view_cls.as_view(path.endpoint_name, *view_args, **view_kwargs)

    app.add_url_rule(path.base_url, defaults={path.pk_name: None}, view_func=view_func, methods=['GET'])
    app.add_url_rule(path.base_url, view_func=view_func, methods=['POST'])
    app.add_url_rule(f"{path.base_url}<{path.pk_type}:{path.pk_name}>",
                     view_func=view_func,
                     methods=['GET', 'PATCH', 'DELETE'])
