#  BSD 3-Clause License
#
#  Copyright (c) 2012, the Sentry Team, see AUTHORS for more details
#  Copyright (c) 2019, Elasticsearch BV
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE


import re

from apitracker_agent.conf.constants import ERROR, MASK, SPAN, TRANSACTION, EVENT
from apitracker_agent.utils import compat, varmap
from apitracker_agent.utils.encoding import force_text

SANITIZE_FIELD_NAMES = frozenset(
    ["authorization", "password", "secret", "passwd", "password", "token", "api_key", "access_token", "sessionid"]
)

SANITIZE_VALUE_PATTERNS = [re.compile(r"^[- \d]{16,19}$")]  # credit card numbers, with or without spacers


def for_events(*events):
    """
    :param events: list of event types

    Only calls wrapped function if given event_type is in list of events
    """
    events = set(events)

    def wrap(func):
        func.event_types = events
        return func

    return wrap


def remove_http_request_body(client, event):
    """
    Removes request.body from context

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    if "context" in event and "request" in event:
        event["request"].pop("body", None)
    return event


def sanitize_http_request_cookies(client, event):
    """
    Sanitizes http request cookies

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """

    # sanitize request.cookies dict
    try:
        cookies = event["request"]["cookies"]
        event["request"]["cookies"] = varmap(_sanitize, cookies)
    except (KeyError, TypeError):
        pass

    # sanitize request.header.cookie string
    try:
        cookie_string = event["request"]["headers"]["cookie"]
        event["request"]["headers"]["cookie"] = _sanitize_string(cookie_string, "; ", "=")
    except (KeyError, TypeError):
        pass
    return event


def sanitize_http_response_cookies(client, event):
    """
    Sanitizes the set-cookie header of the response
    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        cookie_string = event["response"]["headers"]["set-cookie"]
        event["response"]["headers"]["set-cookie"] = _sanitize_string(cookie_string, ";", "=")
    except (KeyError, TypeError):
        pass
    return event


def sanitize_http_headers(client, event):
    """
    Sanitizes http request/response headers

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    # request headers
    try:
        headers = event["request"]["headers"]
        event["request"]["headers"] = varmap(_sanitize, headers)
    except (KeyError, TypeError):
        pass

    # response headers
    try:
        headers = event["response"]["headers"]
        event["response"]["headers"] = varmap(_sanitize, headers)
    except (KeyError, TypeError):
        pass

    return event


def sanitize_http_wsgi_env(client, event):
    """
    Sanitizes WSGI environment variables

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        env = event["request"]["env"]
        event["request"]["env"] = varmap(_sanitize, env)
    except (KeyError, TypeError):
        pass
    return event


def sanitize_http_request_querystring(client, event):
    """
    Sanitizes http request query string

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        path = force_text(event["request"]["query"], errors="replace")
    except (KeyError, TypeError):
        return event
    if "=" in path:
        sanitized_query_string = _sanitize_string(path, "&", "=")
        event["request"]["query"] = sanitized_query_string
    return event

@for_events(EVENT)
def sanitize_http_request_body(client, event):
    """
    Sanitizes http request body. This only works if the request body
    is a query-encoded string. Other types (e.g. JSON) are not handled by
    this sanitizer.

    :param client: an apitracker_agent client
    :param event: a transaction or error event
    :return: The modified event
    """
    try:
        body = force_text(event["request"]["body"], errors="replace")
    except (KeyError, TypeError):
        return event
    if "=" in body:
        sanitized_query_string = _sanitize_string(body, "&", "=")
        event["request"]["body"] = sanitized_query_string
    return event


def _sanitize(key, value):
    if value is None:
        return

    if isinstance(value, compat.string_types) and any(pattern.match(value) for pattern in SANITIZE_VALUE_PATTERNS):
        return MASK

    if isinstance(value, dict):
        # varmap will call _sanitize on each k:v pair of the dict, so we don't
        # have to do anything with dicts here
        return value

    if not key:  # key can be a NoneType
        return value

    key = key.lower()
    for field in SANITIZE_FIELD_NAMES:
        if field in key:
            # store mask as a fixed length for security
            return MASK
    return value


def _sanitize_string(unsanitized, itemsep, kvsep):
    """
    sanitizes a string that contains multiple key/value items
    :param unsanitized: the unsanitized string
    :param itemsep: string that separates items
    :param kvsep: string that separates key from value
    :return: a sanitized string
    """
    sanitized = []
    kvs = unsanitized.split(itemsep)
    for kv in kvs:
        kv = kv.split(kvsep)
        if len(kv) == 2:
            sanitized.append((kv[0], _sanitize(kv[0], kv[1])))
        else:
            sanitized.append(kv)
    return itemsep.join(kvsep.join(kv) for kv in sanitized)
