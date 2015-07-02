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
        vertex = self.client.add_vertex()
        self.assertIsNotNone(vertex)

    def test_create_node_label(self):
        vertex = self.client.add_vertex("test")
        self.assertEqual(vertex.label, "test")

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
        edge = self.client.edge(7)
        self.assertEqual(edge.id, 7)

    def test_get_edge_id_doesntexist(self):
        vertex = self.client.edge(10000)
        self.assertIsNone(vertex)

    def test_get_edges(self):
        resp = self.client.edges()
        self.assertTrue(len(resp) > 0)

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

    def test_set_edge_property(self):
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

    def test_edge_create(self):
        node1 = self.client.add_vertex()
        id1 = node1.id
        node2 = self.client.add_vertex()
        id2 = node2.id
        edge = node1.add_edge("knows", node2)
        self.assertEqual(edge.out_vertex().id, id1)
        self.assertEqual(edge.in_vertex().id, id2)

    def test_out_edges(self):
        node = self.client.vertex(1)
        resp = node.out_edges()
        self.assertEqual(len(resp), 3)

    def test_in_edges(self):
        node = self.client.vertex(3)
        resp = node.in_edges()
        self.assertEqual(len(resp), 3)

    def test_both_edges(self):
        node = self.client.vertex(3)
        resp = node.edges()
        self.assertEqual(len(resp), 3)


if __name__ == "__main__":
    unittest.main()
