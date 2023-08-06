import json 

from sqlalchemy import types, String


class JSONArray(types.TypeDecorator):
    impl = String()

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


class Choices(types.TypeDecorator):
    impl = String()

    