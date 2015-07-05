"""Implements the API specified in
https://github.com/escalant3/pyblueprints/blob/master/pyblueprints/base.py"""
from gremlinrestclient.client import GraphDatabase
from gremlinrestclient.element import Element, Vertex, Edge


__all__ = ("PyBlueprintsGraphDatabase", "BlueprintsElement", "BlueprintsVertex",
           "BlueprintsEdge")


class BlueprintsElement(Element):
    """An abstract class defining an Element object composed
    by a collection of key/value properties"""

    def getProperty(self, key):
        return self.property(key)

    def getPropertyKeys(self):
        return self.keys()

    def setProperty(self, key, value):
        """Sets the property of the element to the given value
        @params key: The property key to set
        @params value: The value to set"""
        return self.property(key, value=value)

    def getId(self):
        return self.get_id()

    def removeProperty(self, key):
        """Removes the value of the property for the given key
        @params key: The key which value is being removed"""
        self.remove_property(key)


class BlueprintsVertex(Vertex, BlueprintsElement):
    """Vertex object impementing pyblueprints style interface."""

    def getOutEdges(self, label=None):
        return self.out_edges(label=label)

    def getInEdges(self, label=None):
        return self.in_edges(label=label)

    def getBothEdges(self, label=None):
        return self.edges(label=label)


class BlueprintsEdge(Edge, BlueprintsElement):
    """An abstract class defining a Edge object representing
    a relationship of the graph with a set of properties"""

    def getOutVertex(self):
        return self.out_vertex()

    def getInVertex(self):
        return self.in_vertex()

    def getLabel(self):
        return self._label


class PyBlueprintsGraphDatabase(GraphDatabase):
    """A Blueprints-like API in Python. Used to bind to legacy
    implementations"""
    def __init__(self, url="http://localhost:8182"):
        super(PyBlueprintsGraphDatabase, self).__init__(
            vertex_class=BlueprintsVertex, edge_class=BlueprintsEdge)

    def addVertex(self, _id=None):
        return self.add_vertex(_id)

    def getVertex(self, _id):
        return self.vertex(_id)

    def getVertices(self):
        return self.vertices()

    def removeVertex(self, vertex):
        vertex.remove()

    def addEdge(self, outVertex, inVertex, label):
        edge = outVertex.add_edge(label, inVertex)
        return edge

    def getEdge(self, _id):
        return self.edge(_id)

    def getEdges(self):
        return self.edges()

    def removeEdge(self, edge):
        edge.remove()

    def clear(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")

    def shutdown(self):
        """TODO Documentation"""
        raise NotImplementedError("Method has to be implemented")
