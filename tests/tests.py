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
        resp = self.client.add_vertex()
        # print(resp)

    def test_create_node_label(self):
        resp = self.client.add_vertex("test")
        # print(resp)

    def test_get_vertex(self):
        v = self.client.vertex(1)
        self.assertEqual(v.id, 1)

    def test_get_vertex_id_doesntexist(self):
        v = self.client.vertex(10000000)
        self.assertIsNone(v)

    def test_get_vertices(self):
        vs = self.client.vertices()
        self.assertIsNotNone(vs)

    def test_get_edge(self):
        resp = self.client.edge(7)
        # print(resp)

    def test_get_edge_id_doesntexist(self):
        resp = self.client.edge(10000)
        # print(resp)

    def test_get_edges(self):
        resp = self.client.edges()
        # print([r.id for r in resp])

    def test_get_node_property(self):
        v = self.client.vertex(1)
        p = v.property('name')
        self.assertEqual(p, "marko")

    def test_set_node_property(self):
        v = self.client.vertex(1)
        p = v.property('name', 'dave')
        v = self.client.vertex(1)
        p = v.property('name')
        self.assertEqual(p, "dave")
        p = v.property('name', 'marko')
        v = self.client.vertex(1)
        p = v.property('name')
        self.assertEqual(p, "marko")

    def test_get_edge_property(self):
        e = self.client.edge(7)
        p = e.property('weight')
        self.assertEqual(p, 0.5)

    def test_set_node_property(self):
        e = self.client.edge(7)
        e.property('weight', 1.0)
        e = self.client.edge(7)
        p = e.property('weight')
        self.assertEqual(p, 1.0)
        e = self.client.edge(7)
        e.property('weight', 0.5)
        e = self.client.edge(7)
        p = e.property('weight')
        self.assertEqual(p, 0.5)

    def test_edge_in_out_vertex(self):
        edge = self.client.edge(7)
        out = edge.out_vertex()
        self.assertEqual(out.id, 1)
        inv = edge.in_vertex()
        self.assertEqual(inv.id, 2)


if __name__ == "__main__":
    unittest.main()
