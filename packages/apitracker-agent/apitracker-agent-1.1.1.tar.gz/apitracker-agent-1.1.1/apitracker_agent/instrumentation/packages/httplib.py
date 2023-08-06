from apitracker_agent.conf.constants import EVENT
from apitracker_agent.instrumentation.packages.base import BaseInstrumentation
from uuid import uuid4
import time
import base64
from apitracker_agent.context import execution_context

try:
    from httplib import HTTPConnection, HTTPResponse  # type: ignore
except ImportError:
    from http.client import HTTPConnection, HTTPResponse

# Python 2 and 3: alternative 4
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class HttpLibInstrumentation(BaseInstrumentation):
    name = "httplib"

    def instrument(self):
        _install_httplib()


def _install_httplib():
    real_request = HTTPConnection._send_request
    real_getresponse = HTTPConnection.getresponse
    real_readresponse = HTTPResponse.read

    # hook into sendrequest and set up a partial event object.
    # the event object is store in the HTTPConnection object itself so it can be referenced in getresponse below
    def _sendrequest(self, method, url, body=None, headers={},
                     encode_chunked=False):
        host = self.host

        client = execution_context.get_client()
        if client is None or host not in client.config.api_ids:
            return real_request(self, method, url, body, headers, encode_chunked)

        port = self.port
        default_port = self.default_port
        real_url = url
        parsed_url = urlparse(url)

        if not real_url.startswith(("http://", "https://")):
            real_url = "%s://%s%s%s" % (
                default_port == 443 and "https" or "http",
                host,
                port != default_port and ":%s" % port or "",
                url,
            )
        request_received_at = int(round(time.time() * 1000000000))

        headers = dict(headers)
        headers['Host'] = host
        self._apitracker_context = {
            "event": {
                "eventId": uuid4(),
                "apiId": client.config.api_ids[host],
                "request": {
                    "method": method,
                    "headers": headers,
                    "body": base64.b64encode(body.encode('utf-8')) if body is not None else None,
                    "url": real_url,
                    "path": parsed_url.path,
                    "query": parsed_url.query,
                    "receivedAt": request_received_at
                }
            },
            "client": client
        }
        return real_request(self, method, url, body, headers, encode_chunked)

    # Hook into getresponse to further construct the event object that was started in _sendrequest.
    # We can't read response body here because it'll close the body. We need to hook into HTTPResponse.read for that.
    # So we have to save the event to the response object so when read is called, we can reference the event
    def getresponse(self, *args, **kwargs):
        apitracker_context = getattr(self, "_apitracker_context", None)

        if apitracker_context is None:
            return real_getresponse(self, *args, **kwargs)
        rv = real_getresponse(self, *args, **kwargs)

        response_received_at = int(round(time.time() * 1000000000))
        apitracker_context['event']['response'] = {
            "headers": dict(rv.headers),
            "statusCode": rv.status,
            "receivedAt": response_received_at
        }
        rv._apitracker_context = apitracker_context
        return rv

    def readresponse(self, amt=None):
        rv = real_readresponse(self, amt)

        apitracker_context = getattr(self, "_apitracker_context", None)
        if apitracker_context is None or 'queued' in apitracker_context:
            return rv

        apitracker_context['event']['response']['body'] = base64.b64encode(rv) if rv else None
        apitracker_context['client'].queue(EVENT, apitracker_context['event'])
        # mark the event as queued so multiple read don't result in multiple events
        apitracker_context['queued'] = True

        return rv

    HTTPConnection._send_request = _sendrequest
    HTTPConnection.getresponse = getresponse
    HTTPResponse.read = readresponse
