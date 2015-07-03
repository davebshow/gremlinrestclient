import unittest
from gremlinrestclient import (GremlinRestClient, GremlinServerError,
                               GraphDatabase, BlueprintsGraphDatabase)


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
        self.assertGreater(len(vs), 0)

    def test_get_edge(self):
        edge = self.client.edge(7)
        self.assertEqual(edge.id, 7)

    def test_get_edge_id_doesntexist(self):
        vertex = self.client.edge(10000)
        self.assertIsNone(vertex)

    def test_get_edges(self):
        resp = self.client.edges()
        self.assertGreater(len(resp),  0)

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

    # def test_out_edges_filter(self):
    #     node = self.client.vertex(1)
    #     resp = node.out_edges(label='')
    #     # self.assertEqual(len(resp), 3)
    #     print(resp)

    def test_in_edges(self):
        node = self.client.vertex(3)
        resp = node.in_edges()
        self.assertEqual(len(resp), 3)

    def test_both_edges(self):
        node = self.client.vertex(3)
        resp = node.edges()
        self.assertEqual(len(resp), 3)

    def test_node_remove(self):
        node = self.client.add_vertex()
        vid = node.id
        node = self.client.vertex(vid)
        self.assertTrue(node.id, vid)
        node.remove()
        node = self.client.vertex(vid)
        self.assertIsNone(node)

    def test_edge_remove(self):
        node = self.client.add_vertex()
        node2 = self.client.add_vertex()
        vid = node.id
        vid2 = node2.id
        edge = node.add_edge("knows", node2)
        eid = edge.id
        self.assertEqual(edge.out_vertex().id, vid)
        self.assertEqual(edge.in_vertex().id, vid2)
        # Test with real db
        edge = self.client.edge(eid)
        self.assertEqual(edge.id, eid)
        edge.remove()
        edge = self.client.edge(eid)
        self.assertIsNone(edge)

    def test_remove_property(self):
        node = self.client.add_vertex()
        node.property("name", "josema")
        name = node.property("name")
        self.assertEqual(name, "josema")
        name = node.remove_property("name")
        name = node.property("name")
        self.assertIsNone(name)


class PyblueprintsTestCase(unittest.TestCase):

    def setUp(self):
        self.client = BlueprintsGraphDatabase()

    def test_addVertex(self):
        v = self.client.addVertex()
        self.assertIsNotNone(v)

    def test_getVertex(self):
        v = self.client.getVertex(1)
        self.assertEqual(v.id, 1)

    def test_getVertices(self):
        vs = self.client.getVertices()
        self.assertGreater(len(vs), 0)

    def test_addEdge(self):
        v1 = self.client.addVertex()
        v2 = self.client.addVertex()
        edge = self.client.addEdge(v1, v2, "knows")
        # Wierd
        eid = edge.id
        e = self.client.getEdge(eid)
        self.assertEqual(eid, e.id)

    def test_getEdge(self):
        e = self.client.getEdge(7)
        self.assertTrue(e.id, 7)

    def test_getEdges(self):
        resp = self.client.getEdges()
        self.assertGreater(len(resp), 0)

    def test_node_remove(self):
        node = self.client.addVertex()
        vid = node.id
        node = self.client.getVertex(vid)
        self.assertEqual(node.id, vid)
        self.client.removeVertex(node)
        node = self.client.getVertex(vid)
        self.assertIsNone(node)

    def test_edge_remove(self):
        node = self.client.addVertex()
        node2 = self.client.addVertex()
        vid = node.id
        vid2 = node2.id
        edge = self.client.addEdge(node, node2, "knows")
        eid = edge.id
        self.assertEqual(edge.getOutVertex().id, vid)
        self.assertEqual(edge.getInVertex().id, vid2)
        # Test with real db
        edge = self.client.getEdge(eid)
        self.assertEqual(edge.id, eid)
        edge.remove()
        edge = self.client.getEdge(eid)
        self.assertIsNone(edge)

    def test_getPropertysetProperty(self):
        node = self.client.getVertex(1)
        name = node.getProperty("name")
        self.assertEqual("marko", name)
        node.setProperty("name", "dave")
        node = self.client.getVertex(1)
        name = node.getProperty("name")
        self.assertEqual("dave", name)
        node.setProperty("name", "marko")
        node = self.client.getVertex(1)
        name = node.getProperty("name")
        self.assertEqual("marko", name)

    def test_getPropertyKeys(self):
        node = self.client.getVertex(1)
        keys = node.getPropertyKeys()
        self.assertGreater(len(keys), 1)

    def test_getId(self):
        node = self.client.getVertex(1)
        self.assertEqual(node.getId(), 1)

    def test_remove_property(self):
        node = self.client.addVertex()
        node.setProperty("name", "josema")
        name = node.getProperty("name")
        self.assertEqual(name, "josema")
        name = node.removeProperty("name")
        name = node.getProperty("name")
        self.assertIsNone(name)

    def test_outEdges(self):
        node = self.client.getVertex(1)
        resp = node.getOutEdges()
        self.assertEqual(len(resp), 3)

    def test_getInEdges(self):
        node = self.client.getVertex(3)
        resp = node.getInEdges()
        self.assertEqual(len(resp), 3)

    def test_getBothEdges(self):
        node = self.client.getVertex(3)
        resp = node.getBothEdges()
        self.assertEqual(len(resp), 3)

    def test_edge_in_out_vertex(self):
        edge = self.client.getEdge(7)
        out = edge.getOutVertex()
        self.assertEqual(out.id, 1)
        inv = edge.getInVertex()
        self.assertEqual(inv.id, 2)

    def test_getLabel(self):
        edge = self.client.getEdge(7)
        self.assertEqual(edge.getLabel(), 'knows')


if __name__ == "__main__":
    unittest.main()
