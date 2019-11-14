import requests
from urllib3 import Retry

from core.exceptions import HttpError


def get_subclass(cls, field_name, field_value):
    for subclass in cls.__subclasses__():
        if field_value == getattr(subclass, field_name, None):
            return subclass
        found = get_subclass(subclass, field_name, field_value)
        if found:
            return found


def _requests_retry_session(session=None, retries=3):
    from requests.adapters import HTTPAdapter

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=0.3,
        status_forcelist=(504,),
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def __handle_requests_exception(requests_exception):
    response = requests_exception.response

    error_cls: HttpError = get_subclass(HttpError, 'http_code', response.status_code)
    if error_cls:
        return error_cls
    else:
        return HttpError(response=response)


def post(url, data=None, json=None, **kwargs):
    session = _requests_retry_session()
    try:
        response = session.post(url, data=data, json=json, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as httpe:
        raise __handle_requests_exception(httpe)
    finally:
        session.close()
