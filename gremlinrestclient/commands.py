class CommandsMixin(object):
    """
    Some useful commands for the Gremlin Server.
    """

    def add_vertex(self, label=None):
        """
        Adds a new vertex to the graph.

        :params str label: Node label (optional)

        :returns: The created Vertex
        """

        if label is not None:
            script = """graph.addVertex(label, vertex_label)"""
            bindings = {"vertex_label": label}
        else:
            script = """graph.addVertex()"""
            bindings = {}
        resp = self.execute(script, bindings=bindings)
        vertex = self.make_elem(resp, Vertex)
        return vertex

    def vertex(self, vid):
        """Retrieves an existing vertex from the graph
        :params int vid: Node unique identifier

        :returns: The requested Vertex or None"""
        script = """g.V(vid)"""
        bindings = {"vid": vid}
        resp = self.execute(script, bindings=bindings)
        vertex = self.make_elem(resp, Vertex)
        return vertex

    def make_elem(self, resp, elem_class):
        try:
            data = resp.data[0]
        except IndexError:
            elem = None
        else:
            elem = elem_class(data, self)
        return elem

    def vertices(self):
        """Returns an iterator with all the vertices"""
        script = """g.V()"""
        resp = self.execute(script)
        vertices = [Vertex(v, self) for v in resp.data]
        return vertices

    def edge(self, eid):
        """Retrieves an existing edge from the graph
        :params str eid: Edge unique identifier

        :returns: The requested Edge or None"""
        # Bindings don't seem to work here...
        script = """g.E(%s)""" % (eid)
        resp = self.execute(script)
        edge = self.make_elem(resp, Edge)
        return edge

    def edges(self):
        """Returns an iterator with all the edges"""
        script = """g.E()"""
        resp = self.execute(script)
        edges = [Edge(e, self) for e in resp.data]
        return edges


class Element(object):
    """An abstract class defining an Element object composed
    by a collection of key/value properties"""

    def __init__(self, element_data, gdb):
        self._gdb = gdb
        self._eid = element_data["id"]
        self._properties = element_data["properties"]
        self._type = element_data["type"]
        self._label = element_data["label"]
        self._source = ""

    @property
    def label(self):
        return self._label

    @property
    def id(self):
        return self._eid

    @property
    def properties(self):
        return self._properties

    def _get_script(self):
        raise NotImplementedError

    def values(self, prop):
        get_script, bindings = self._get_script()
        script = """%selem.values(prop);""" % (get_script)
        bindings.update({"prop": prop})
        resp = self._gdb.execute(script, bindings=bindings)
        try:
            prop = resp.data[0]
        except IndexError:
            prop = None
        return prop

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
                output = self._gdb.make_elem(resp, Vertex)
            else:
                print(resp)
                output = self._gdb.make_elem(resp, Edge)
        else:
            output = self.values(key)
        return output

    def _set_property_script(self, prop, value):
        get_script, bindings = self._get_script()
        script = """%selem.property(prop, val);""" % (get_script)
        bindings.update({"prop": prop, "val": value})
        return script, bindings

    def keys(self):
        """Returns a set with the property keys of the element

        :returns: Set of property keys"""
        return self._properties.keys()

    def get_id(self):
        """Returns the unique identifier of the element

        @returns The unique identifier of the element"""
        return self._eid

    def remove(self):
        get_script, bindings = self._get_script()
        script = """%s;elem.remove;""" % (get_script)
        self._gdb.execute(script, binding=bindings)


class Vertex(Element):
    """An abstract class defining a Vertex object representing
    a node of the graph with a set of properties"""

    def __init__(self, vertex, gdb):
        super(Vertex, self).__init__(vertex, gdb)
        self._source = "V"

    def _get_script(self):
        script = """elem = g.%s(eid);""" % (self._source)
        bindings = {"eid": self._eid}
        return script, bindings

    def add_edge(self):
        pass

    def out_edges(self, label=None):
        """Gets all the outgoing edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

    def in_edges(self, label=None):
        """Gets all the incoming edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

    def edges(self, label=None):
        """Gets all the edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")


class Edge(Element):
    """An abstract class defining a Edge object representing
    a relationship of the graph with a set of properties"""

    def __init__(self, edge, gdb):
        super(Edge, self).__init__(edge, gdb)
        self._source = "E"
        self._out_vertex = edge["outV"]
        self._in_vertex = edge["inV"]
        self._out_label = edge["outVLabel"]
        self._out_label = edge["inVLabel"]

    def _get_script(self):
        # A hack because bindings aren't working with edge lookups
        script = """elem = g.%s(%s);""" % (self._source, self._eid)
        bindings = {}
        return script, bindings

    def out_vertex(self):
        """Returns the origin Vertex of the relationship

        :returns: The origin Vertex"""
        return self._get_vertex(self._out_vertex)

    def in_vertex(self):
        """Returns the target Vertex of the relationship

        :returns: The target Vertex"""
        return self._get_vertex(self._in_vertex)

    def _get_vertex(self, vid):
        script = """g.V(vid)"""
        bindings = {"vid": vid}
        resp = self._gdb.execute(script, bindings=bindings)
        vertex = self._gdb.make_elem(resp, Vertex)
        return vertex
