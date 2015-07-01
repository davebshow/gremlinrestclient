import unittest
from gremlinrestclient import (GremlinRestClient, GremlinServerError,
                               GraphDatabase)


class GremlinRestClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = GremlinRestClient()

    def test_request(self):
        resp = self.client.execute("1 + 1")
        self.assertEqual(resp.data[0], 2)

    def test_bindings(self):
        resp = self.client.execute("x + x", bindings={"x": 1})
        self.assertEqual(resp.data[0], 2)

    def test_error(self):
        try:
            self.client.execute("x + x.fasdfewq", bindings={"x": 1})
            error = False
        except GremlinServerError:
            error = True
        self.assertTrue(error)


class GraphDatabaseCommandsTestCase(unittest.TestCase):

    def setUp(self):
        self.client = GraphDatabase()

    def test_create_node(self):
        resp = self.client.addVertex()
        # print(resp)

    def test_create_node_label(self):
        resp = self.client.addVertex("test")
        # print(resp)

    def test_get_vertex(self):
        resp = self.client.getVertex(1)
        print(resp)

    def test_get_vertex_id_doesntexist(self):
        resp = self.client.getVertex(100)
        print(resp)

    def test_get_vertices(self):
        resp = self.client.getVertices()
        print(resp)

    def test_get_edge(self):
        resp = self.client.getEdge(1)
        print(resp)

    def test_get_edge_id_doesntexist(self):
        resp = self.client.getEdge(100)
        print(resp)

    def test_get_edges(self):
        resp = self.client.getEdges()
        print(resp)


if __name__ == "__main__":
    unittest.main()
