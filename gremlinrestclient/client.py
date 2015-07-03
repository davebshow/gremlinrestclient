import collections
import json

import requests

from gremlinrestclient.exceptions import RequestError, GremlinServerError
from gremlinrestclient.element import Vertex, Edge


__all__ = ("GremlinRestClient", "GraphDatabase", "Response")

Response = collections.namedtuple(
    "Response",
    ["status_code", "data", "message", "metadata"])


class GremlinRestClient(object):

    HEADERS = {'content-type': 'application/json'}

    def __init__(self, url="http://localhost:8182"):
        self._url = url

    def execute(self, gremlin, bindings=None, lang="gremlin-groovy"):
        """
        Send a script to the Gremlin Server

        :param str gremlin: The script to send.
        :param dict bindings: Bindings for the Gremlin Script.
        :param str lang: Gremlin language variant.

        :returns: :py:class:`Response<gremlinrestclient.client.Response>`
        """
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


class GraphDatabase(GremlinRestClient):
    """
    A high level interface for the Gremlin Server.
    """
    def __init__(self, url="http://localhost:8182", edge_class=Edge,
                 vertex_class=Vertex):
        super(GraphDatabase, self).__init__(url=url)
        self._edge_class = edge_class
        self._vertex_class = vertex_class

    def add_vertex(self, label=None):
        """
        Adds a new vertex to the graph.

        :params str label: Node label (optional)

        :returns: The created
            :py:class:`Vertex<gremlinrestclient.element.Vertex>`
        """

        if label is not None:
            script = """graph.addVertex(label, vertex_label)"""
            bindings = {"vertex_label": label}
        else:
            script = """graph.addVertex()"""
            bindings = {}
        resp = self.execute(script, bindings=bindings)
        vertex = self._make_elem(resp, self._vertex_class)
        return vertex

    def vertex(self, vid):
        """Get an existing vertex from the graph

        :params int vid: Unique node identifier
        :returns: The requested :py:class:`gremlinrestclient.element.Vertex`
            or None
        """
        script = """g.V(vid)"""
        bindings = {"vid": vid}
        resp = self.execute(script, bindings=bindings)
        vertex = self._make_elem(resp, self._vertex_class)
        return vertex

    def _make_elem(self, resp, elem_class):
        try:
            data = resp.data[0]
        except IndexError:
            elem = None
        else:
            elem = elem_class(data, self)
        return elem

    def vertices(self):
        """
        Get all vertices in graph.

        :returns: :py:class:`list` of
            :py:class:`Vertex<gremlinrestclient.element.Vertex>` objects
        """
        script = """g.V()"""
        resp = self.execute(script)
        vertices = [self._vertex_class(v, self) for v in resp.data]
        return vertices

    def edge(self, eid):
        """Retrieves an existing edge from the graph

        :params str eid: Unique edge identifier

        :returns: The requested
            :py:class:`Edge<gremlinrestclient.element.Edge>` or None
        """
        # Bindings don't seem to work here...
        script = """g.E(%s)""" % (eid)
        resp = self.execute(script)
        edge = self._make_elem(resp, self._edge_class)
        return edge

    def edges(self):
        """
        Get all edges in graph.

        :returns: :py:class:`list` of
            :py:class:`Edge<gremlinrestclient.element.Edge>`
        """
        script = """g.E()"""
        resp = self.execute(script)
        print(resp)
        edges = [self._edge_class(e, self) for e in resp.data]
        return edges
