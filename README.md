# Gremlin REST Client
An HTTP client for the Gremlin server.

## Features

* An easy to use client class GremlinRestClient that allows you to submit scripts to the Gremlin Server.
* A a series of mid-level classes that all inherit from GremlinRestClient and Graph. These classes correspond to various Tinkerpop 3 vendor implementations and provide convenience methods for creating indices, schemas, etc.
* The Create API, utilized by the Graph classes. Allows for easy programmatic creation of nodes and edges using Python dict and tuple.

## Installation
Install using `pip`.

```
$ pip install gremlinrestclient
```

## Getting Started
Run a script to add a vertex to the graph.

```
>>> import gremlinrestclient
>>> client = gremlinrestclient.GremlinRestClient()
>>> resp = client.execute(
...     "graph.addVertex(label, p1, 'name', p2)",
...     bindings={"p1": "person", "p2": "dave"})
>>> resp
Response(status_code=200, data=[{u'properties': {u'name': [{u'id': 226, u'value': u'dave'}]}, u'type': u'vertex', u'id': 225, u'label': u'person'}], message={}, metadata=u'')
```

### Create API
The Graph subclasses use the Create API to make the creation of nodes and edges easier. In the spirit of keeping it simple, nodes are dict objects. It is important to note that the key `label` always refers to the optional node label, and if the key `id` is passed it will be clobbered. If you need a property called `id`, consider using `_id` instead.

Consider the following example:

```
>>> graph = gremlinrestclient.TinkerGraph()
>>> d = {"name": "dave", "label": "person"}
>>> coll = graph.create(d)
>>> coll
Collection(
    vertices=(
        Vertex(id=227, label=u'person', properties={u'name': [{u'id': 228, u'value': u'dave'}]}),), edges=())
>>> vertex.vertices
(Vertex(id=227, label=u'person', properties={u'name': [{u'id': 228, u'value': u'dave'}]}),)
```

The create method returns a namedtuple called Collection. Collection contains two fields, vertices and edges, which are tuples of Vertex and Edge objects respectively. Lot’s of tuples.

To create edges, we use more tuple (not to be confused with the namedtuple Vertex). Observe:

```
>>> d = {"name": "dave", "label": "person"}
>>> p = {"name": "python", "label": "lang"}
>>> e = (d, "LIKES", p, {'weight': 1})
>>> graph.create(e)
Collection(
    vertices=(
        Vertex(id=248, label=u'person', properties={u'name': [{u'id': 249, u'value': u'dave'}]}),
        Vertex(id=250, label=u'lang', properties={u'name': [{u'id': 251, u'value': u'python'}]})),
    edges=(
        Edge(id=252, source_id=248, label=u'LIKES', target_id=250, properties={u'weight': 1}),))
```

Edge tuples are always the same (source, label, target, properties), but there are several ways to pass the source and target nodes to the tuple list. Instead of passing a node dictionary directly to an edge, you can pass the node dictionary as an argument, and pass its index to the edge tuple:

```
>>> p = {"name": "python", "label": "lang"}
>>> graph.create({"name": "dave", "label": "person"}, (0, "LIKES", p, {'weight': 1}))
Collection(
    vertices=(
        Vertex(id=229, label=u'person', properties={u'name': [{u'id': 230, u'value': u'dave'}]}),
        Vertex(id=231, label=u'lang', properties={u'name': [{u'id': 232, u'value': u'python'}]})),
    edges=(
        Edge(id=233, source_id=229, label=u'LIKES', target_id=231, properties={}),))
```

Here, the 0 in the edge tuple simple refers to the zeroith argument passed to the create() method.

Finally, you can pass a gremlinrestclient.graph.Vertex object (or two) to the edge tuple. Check:

```
>>> d = {"name": "dave", "label": "person"}
>>> coll = graph.create(d)
>>> dave, = coll.vertices  # Unpack tuple of length 1
>>> graph.create(
...     {"name": "python", "label": "lang"},
...     (dave, "LIKES", 0, {'weight': 1}))
Collection(
    vertices=(
        Vertex(id=261, label=u'lang', properties={u'name': [{u'id': 262, u'value': u'python'}]}),),
    edges=(
        Edge(id=263, source_id=259, label=u'LIKES', target_id=261, properties={u'weight': 1}),))
```

Note that only newly created nodes and edges are created in the collection.

## Contribute

Contributions are welcome. If you find a bug, or have a suggestion, please open an issue on Github. If you would like to make a pull request, please make sure to add appropriate tests and run them:

```
$ python setup.py test
```

In the future there will be CI and more info on contributing.
