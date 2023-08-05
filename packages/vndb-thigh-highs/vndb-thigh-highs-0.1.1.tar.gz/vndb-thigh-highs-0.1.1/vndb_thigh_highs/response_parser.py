import json
from enum import Enum
from .error import ResponseError, ResponseErrorId, UnknownResponseError

class ResponseKey(Enum):
    OK = 'ok'
    ERROR = 'error'
    DBSTATS = 'dbstats'
    RESULTS = 'results'

class ResponseParser:
    _common_error_ids = [
        ResponseErrorId.PARSE,
        ResponseErrorId.MISSING,
        ResponseErrorId.BAD_ARG,
        ResponseErrorId.NEED_LOGIN,
        ResponseErrorId.THROTTLED,
    ]

    def __init__(self, expected_type, error_ids=None):
        self.expected_type = expected_type
        self.error_ids = error_ids
        if error_ids is not None:
            self.error_ids.extend(self._common_error_ids)

    def parse(self, response):
        response_type, response_dict = self.split_response(response)
        if response_type != self.expected_type:
            self.parse_error(response_dict)
        else:
            return response_dict

    def split_response(self, response):
        parts = response.split(maxsplit=1)
        response_type = ResponseKey(parts[0])
        if len(parts) == 1:
            return response_type, None
        return response_type, json.loads(parts[1])

    def parse_error(self, response_dict):
        error_id = ResponseErrorId.from_id(response_dict['id'])
        if error_id not in self.error_ids:
            raise UnknownResponseError(response_dict)
        raise error_id.raise_error(response_dict)

class OkResponseParser(ResponseParser):
    def __init__(self, error_ids):
        super().__init__(ResponseKey.OK, error_ids)

    @classmethod
    def for_login(cls):
        return cls([
            ResponseErrorId.AUTH,
            ResponseErrorId.LOGGED_IN,
        ])

    @classmethod
    def for_set(cls):
        return cls([
            ResponseErrorId.SET_TYPE,
        ])

class DBStatsResponseParser(ResponseParser):
    def __init__(self):
        super().__init__(ResponseKey.DBSTATS)

class GetResponseParser(ResponseParser):
    _error_ids = [
        ResponseErrorId.GET_TYPE,
        ResponseErrorId.GET_INFO,
        ResponseErrorId.FILTER,
    ]

    def __init__(self):
        super().__init__(ResponseKey.RESULTS, self._error_ids)
