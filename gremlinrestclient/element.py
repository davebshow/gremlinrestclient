"""Classes for interacting with the Gremlin Server"""

__all__ = ("Vertex", "Edge")


class Element(object):
    """A base class defining an Element object."""

    def __init__(self, element_data, gdb):
        self._gdb = gdb
        self._eid = element_data["id"]
        self._properties = element_data.get("properties", {})
        self._type = element_data["type"]
        self._label = element_data["label"]
        self._source = ""
        self._vertex_class = self._gdb._vertex_class
        self._edge_class = self._gdb._edge_class

    @property
    def label(self):
        return self._label

    def __str__(self):
        return "{0}: {1}".format(self._type, self._eid)

    def __repr__(self):
        return "{0}: {1}".format(self._type, self._eid)

    @property
    def id(self):
        return self._eid

    @property
    def properties(self):
        return self._properties

    def values(self, prop):
        script = """%s;elem.values(prop);""" % (self._get_script())
        bindings = {"prop": prop, "eid": self._eid}
        resp = self._gdb.execute(script, bindings=bindings)
        try:
            prop = resp.data[0]
        except IndexError:
            prop = None
        return prop

    def remove_property(self, key):
        """
        Remove an element property.

        :param str key: The property to remove.
        """
        script = """%s;elem.next().property(prop).remove();
                 """ % (self._get_script())
        bindings = {"prop": key, "eid": self._eid}
        self._gdb.execute(script, bindings=bindings)

    def property(self, key, value=None):
        """Gets/sets the value of the property for the given key

        :param str key: The key which value is being retrieved.

        :param str value: The value to set the property to (optional).
            None by default.
        :returns: The property associated with the key"""
        if value is not None:
            script, bindings = self._set_property_script(key, value)
            resp = self._gdb.execute(script, bindings=bindings)
            if self._type == "vertex":
                output = self._gdb._make_elem(resp, self._vertex_class)
            else:
                output = self._gdb._make_elem(resp, self._edge_class)
        else:
            output = self.values(key)
        return output

    def _set_property_script(self, prop, value):
        script = """%s;elem.property(prop, val);""" % (self._get_script())
        bindings = {"prop": prop, "val": value, "eid": self._eid}
        return script, bindings

    def keys(self):
        """
        Returns a set with the property keys of the element

        :returns: :py:class:`list` of property keys"""
        return self._properties.keys()

    def get_id(self):
        """Returns the unique identifier of the element

        :returns: The unique identifier of the element"""
        return self._eid

    def remove(self):
        script = """%s.next();elem.remove();""" % (self._get_script())
        bindings = {"eid": self._eid}
        self._gdb.execute(script, bindings=bindings)


class Vertex(Element):
    """
    Vertex

    :param dict vertex: Vertex data returned from server
    :param gdb: GraphDatabase instance associated with this vertex.
    """

    def __init__(self, vertex, gdb):
        super(Vertex, self).__init__(vertex, gdb)
        self._source = "V"

    def _get_script(self):
        # Bindings acting wierd for edge lookups...
        script = """elem = g.%s(eid)""" % (self._source)
        return script

    def add_edge(self, label, vertex):
        script = """vert1 = g.V(vid1).next();
                    vert2 = g.V(vid2).next();
                    vert1.addEdge(lab, vert2, "type", "test")"""
        bindings = {"lab": label, "vid1": self._eid, "vid2": vertex.id}
        resp = self._gdb.execute(script, bindings=bindings)
        return self._gdb._make_elem(resp, self._edge_class)

    # Implement label filter
    def out_edges(self, label=None):
        """Gets all the outgoing edges of the node.

        :returns: A list of :py:class:`Edge<gremlinrestclient.element.Edge>`
        """
        return self._edges("out", label=label)

    def in_edges(self, label=None):
        """Gets all the outgoing edges of the node.

        :returns: A list of :py:class:`Edge<gremlinrestclient.element.Edge>`
        """
        return self._edges("in", label=label)

    def edges(self, label=None):
        """Gets all the outgoing edges of the node.

        :param str label: Label to filter the edges (optional)

        :returns: A list of :py:class:`Edge<gremlinrestclient.element.Edge>`
        """
        return self._edges("both", label=label)

    def _edges(self, pattern, label=None):

        if label is None:
            script = """%s; elem.%sE()""" % (self._get_script(), pattern)
            bindings = {"eid": self._eid}
            resp = self._gdb.execute(script, bindings=bindings)
        else:
            script = """%s; elem.%pE(l)""" % (self._get_script(), pattern)
            bindings = {"l": label, "eid": self._eid}
            resp = self._gdb.execute(script, bindings=bindings)
        return [self._edge_class(e, self._gdb) for e in resp.data]


class Edge(Element):
    """
    Edge

    :param dict edge: Edge data returned from server
    :param gdb: GraphDatabase instance associated with this vertex.
    """

    def __init__(self, edge, gdb):
        super(Edge, self).__init__(edge, gdb)
        self._source = "E"
        self._out_vertex = edge["outV"]
        self._in_vertex = edge["inV"]
        self._out_label = edge["outVLabel"]
        self._out_label = edge["inVLabel"]

    def _get_script(self):
        # Bindings acting wierd for edge lookups...
        script = """elem = g.%s().has(id, eid)""" % (self._source)
        return script

    def out_vertex(self):
        """
        Returns the origin Vertex of the relationship.

        :returns: The origin
            :py:class:`Vertex<gremlinrestclient.element.Vertex>`
        """
        return self._get_vertex(self._out_vertex)

    def in_vertex(self):
        """
        Returns the target Vertex of the relationship.

        :returns: The target
            :py:class:`Vertex<gremlinrestclient.element.Vertex>`"""
        return self._get_vertex(self._in_vertex)

    def _get_vertex(self, vid):
        script = """g.V(vid)"""
        bindings = {"vid": vid}
        resp = self._gdb.execute(script, bindings=bindings)
        vertex = self._gdb._make_elem(resp, self._vertex_class)
        return vertex
