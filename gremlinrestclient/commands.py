class CommandsMixin(object):
    """Based on
    https://github.com/escalant3/pyblueprints/blob/master/pyblueprints/base.py
    """

    def addVertex(self, label=None):
        """
        Adds a new vertex to the graph.

        :params str lable: Node label (optional)

        :returns: The created Vertex
        """

        if label is not None:
            script = """graph.addVertex(label, vertex_label)"""
            bindings = {"vertex_label": label}
        else:
            script = """graph.addVertex()"""
            bindings = {}
        resp = self.execute(script, bindings=bindings)
        return resp

    def getVertex(self, vid):
        """Retrieves an existing vertex from the graph
        :params int vid: Node unique identifier

        :returns: The requested Vertex or None"""
        script = """g.V(vid)"""
        bindings = {"vid": vid}
        resp = self.execute(script, bindings=bindings)
        return resp

    def getVertices(self):
        """Returns an iterator with all the vertices"""
        script = """g.V()"""
        resp = self.execute(script)
        return resp

    def getEdge(self, eid):
        """Retrieves an existing edge from the graph
        :params str eid: Edge unique identifier

        :returns: The requested Edge or None"""
        script = """g.E(eid)"""
        bindings = {"eid": eid}
        resp = self.execute(script, bindings=bindings)
        return resp

    def getEdges(self):
        """Returns an iterator with all the edges"""
        script = """g.E()"""
        resp = self.execute(script)
        return resp


class Element():
    """An abstract class defining an Element object composed
    by a collection of key/value properties"""

    def getProperty(self, key):
        """Gets the value of the property for the given key
        @params key: The key which value is being retrieved

        @returns The value of the property with the given key"""
        raise NotImplementedError("Method has to be implemented")

    def getPropertyKeys(self):
        """Returns a set with the property keys of the element

        @returns Set of property keys"""
        raise NotImplementedError("Method has to be implemented")

    def setProperty(self, key, value):
        """Sets the property of the element to the given value
        @params key: The property key to set
        @params value: The value to set"""
        raise NotImplementedError("Method has to be implemented")

    def getId(self):
        """Returns the unique identifier of the element

        @returns The unique identifier of the element"""
        raise NotImplementedError("Method has to be implemented")

    def removeProperty(self, key):
        """Removes the value of the property for the given key
        @params key: The key which value is being removed"""
        raise NotImplementedError("Method has to be implemented")

    def remove(self):
        pass


class Vertex(Element):
    """An abstract class defining a Vertex object representing
    a node of the graph with a set of properties"""

    def addEdge(self):
        pass

    def getOutEdges(self, label=None):
        """Gets all the outgoing edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

    def getInEdges(self, label=None):
        """Gets all the incoming edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")

    def getBothEdges(self, label=None):
        """Gets all the edges of the node. If label
        parameter is provided, it only returns the edges of
        the given label
        @params label: Optional parameter to filter the edges

        @returns A generator function of edges"""
        raise NotImplementedError("Method has to be implemented")


class Edge(Element):
    """An abstract class defining a Edge object representing
    a relationship of the graph with a set of properties"""

    def getOutVertex(self):
        """Returns the origin Vertex of the relationship

        @returns The origin Vertex"""
        raise NotImplementedError("Method has to be implemented")

    def getInVertex(self):
        """Returns the target Vertex of the relationship

        @returns The target Vertex"""
        raise NotImplementedError("Method has to be implemented")

    def getLabel(self):
        """Returns the label of the relationship

        @returns The edge label"""
        raise NotImplementedError("Method has to be implemented")
