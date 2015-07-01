import collections
import json

import requests

from gremlinrestclient.exceptions import RequestError, GremlinServerError
from gremlinrestclient.commands import CommandsMixin


__all__ = ("GremlinRestClient", "GraphDatabase", "Response")

Response = collections.namedtuple(
    "Response",
    ["status_code", "data", "message", "metadata"])


class GremlinRestClient:

    HEADERS = {'content-type': 'application/json'}

    def __init__(self, url="http://localhost:8182"):
        self._url = url

    def execute(self, gremlin, bindings=None, lang="gremlin-groovy"):
        if bindings is None:
            bindings = {}
        payload = {
            "gremlin": gremlin,
            "bindings": bindings,
            "language": lang
        }
        resp = self._post(self._url, json.dumps(payload),
                          self.HEADERS)
        resp = resp.json()
        resp = Response(resp["status"]["code"],
                        resp["result"]["data"],
                        resp["result"]["meta"],
                        resp["status"]["message"])
        return resp

    def _post(self, url, data, headers):
        resp = requests.post(url, data=data, headers=headers)
        if resp.status_code != 200:
            msg = resp.json()["message"]
            if resp.status_code < 500:
                raise RequestError(resp.status_code, msg)
            else:
                raise GremlinServerError(resp.status_code, msg)
        return resp


class GraphDatabase(GremlinRestClient, CommandsMixin):
    pass
