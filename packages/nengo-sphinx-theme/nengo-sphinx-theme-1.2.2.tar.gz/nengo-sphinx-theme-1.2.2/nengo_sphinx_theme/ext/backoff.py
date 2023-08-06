"""
Monkeypatches the Sphinx HTTP request functions to add exponential backoff.

The main use case for this is to avoid server-side rejections caused by too many
requests when running the linkchecker.
"""

import requests

import backoff
from sphinx.util import requests as sphinx_requests
from sphinx.util.requests import get, head


@backoff.on_predicate(backoff.expo, lambda x: x.status_code == 429, max_time=60)
@backoff.on_exception(
    backoff.constant, requests.exceptions.RequestException, max_tries=3,
)
def get_with_backoff(*args, **kwargs):
    return get(*args, **kwargs)


@backoff.on_predicate(backoff.expo, lambda x: x.status_code == 429, max_time=60)
@backoff.on_exception(
    backoff.constant, requests.exceptions.RequestException, max_tries=3,
)
def head_with_backoff(*args, **kwargs):
    return head(*args, **kwargs)


def setup(_):
    sphinx_requests.get = get_with_backoff
    sphinx_requests.head = head_with_backoff
