class BaseError(Exception):
    code = -1
    description = None

    def __init__(self, description=None):
        __message = description or self.description
        super().__init__(__message)


class HttpError(BaseError):
    # http errors starts with 2
    code = 20000
    http_code = None
    description = "Base HTTP Exception"

    def __init__(self, response=None):
        self.response = response
        super().__init__(self.__get_message(response))

    @classmethod
    def __get_message(cls, response):
        return f"{response.status_code}: {response.content}"


class BadRequestError(HttpError):
    code = 20400
    http_code = 400


class NotFoundError(HttpError):
    code = 20404
    http_code = 404


class TooManyRequestsError(HttpError):
    code = 20429
    http_code = 429


class InternalServerError(HttpError):
    code = 20500
    http_code = 500


class ServiceUnavailableError(HttpError):
    code = 20503
    http_code = 503


class GatewayTimeoutError(HttpError):
    code = 20504
    http_code = 504
