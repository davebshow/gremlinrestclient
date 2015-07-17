.. gremlinrestclient documentation master file, created by
   sphinx-quickstart on Wed Jul  1 20:09:52 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
gremlinrestclient
=================

A HTTP client for the Gremlin Server.

**Features:**

- An easy to use client class :py:class:`GremlinRestClient<gremlinrestclient.client.GremlinRestClient>` that allows you to submit scripts to the Gremlin Server.

- A a series of mid-level classes that all inherit from :py:class:`GremlinRestClient<gremlinrestclient.client.GremlinRestClient>` and :py:class:`Graph<gremlinrestclient.graph.Graph>`. These classes correspond to various Tinkerpop 3 vendor implementations and provide convenience methods for creating indices, schemas, etc.

- The :ref:`Create`, utilized by the `Graph` classes. Allows for easy programmatic creation of nodes and edges using Python :py:class:`dict` and :py:class:`tuple`.


Releases
========
The latest release of :py:mod:`gremlinrestclient` is **0.0.6**.


Requirements
============

- Python 2.7-3.4
- Tinkerpop 3 Gremlin Server 3.0.0 (3.0.0.M9 for use with Titan 0.9.0-M2)


Dependencies
============
- requests 2.7.0

Installation
============
Install using pip::

    $ pip install gremlinrestclient


Getting Started
===============

Use the simple client:
:py:class:`GremlinRestClient<gremlinrestclient.client.GremlinRestClient>`.


Minimal Example
---------------
Submit a script to the Gremlin Server::

    >>> import gremlinrestclient
    >>> client = gremlinrestclient.GremlinRestClient()
    >>> resp = client.execute(
    ...     "graph.addVertex(label, p1, 'name', p2)",
    ...     bindings={"p1": "person", "p2": "dave"})
    >>> resp
    Response(status_code=200, data=[{u'properties': {u'name': [{u'id': 226,
    u'value': u'dave'}]}, u'type': u'vertex', u'id': 225, u'label': u'person'}],
    message={}, metadata=u'')


.. _Create:

Create API
----------
The :py:class:`Graph<gremlinrestclient.graph.Graph>` subclasses use the Create
API to make the creation of nodes and edges easier. In the spirit of keeping it
simple, nodes are :py:class:`dict` objects. It is important to note that the key
"label" always refers to the optional node label, and if the key "id" is passed
it will be clobbered. If you need a property called "id", consider using "_id" instead.

Consider the following example::

    >>> graph = gremlinrestclient.TinkerGraph()
    >>> d = {"name": "dave", "label": "person"}
    >>> coll = graph.create(d)
    >>> coll
    Collection(
        vertices=(
            Vertex(id=227, label=u'person', properties={u'name': [{u'id': 228, u'value': u'dave'}]}),), edges=())
    >>> vertex.vertices
    (Vertex(id=227, label=u'person', properties={u'name': [{u'id': 228, u'value': u'dave'}]}),)

The :py:meth:`create<gremlinrestclient.graph.Graph.create>` method returns a
namedtuple called :py:class:`Collection<gremlinrestclient.graph.Collection>`.
:py:class:`Collection<gremlinrestclient.graph.Collection>` contains two fields,
``vertices`` and ``edges``, which are tuples of :py:class:`Vertex<gremlinrestclient.graph.Vertex>`
and :py:class:`Edge<gremlinrestclient.graph.Edge>` objects respectively. Lot's of tuples.

To create edges, we use more :py:class:`tuple` (not to be confused with the
namedtuple :py:class:`Vertex<gremlinrestclient.graph.Vertex>`). Observar::

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

Edge tuples are always the same ``(source, label, target, properties)``, but there are several
ways to pass the source and target nodes to the tuple list. Instead of passing a node dictionary
directly to an edge, you can pass the node dictionary as an argument, and pass its index
to the edge tuple::

    >>> p = {"name": "python", "label": "lang"}
    >>> graph.create({"name": "dave", "label": "person"}, (0, "LIKES", p, {'weight': 1}))
    Collection(
        vertices=(
            Vertex(id=229, label=u'person', properties={u'name': [{u'id': 230, u'value': u'dave'}]}),
            Vertex(id=231, label=u'lang', properties={u'name': [{u'id': 232, u'value': u'python'}]})),
        edges=(
            Edge(id=233, source_id=229, label=u'LIKES', target_id=231, properties={}),))

Here, the ``0`` in the edge tuple simple refers to the zeroith argument passed to the
:py:meth:`create` method.

Finally, you can pass a :py:class:`gremlinrestclient.graph.Vertex` object (or two) to the
edge tuple. Check::

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

Note that only newly created nodes and edges are created in the collection.


Contribute
----------

Contributions are welcome. If you find a bug, or have a suggestion, please open
an issue on `Github`_. If you would like to make a pull request, please make
sure to add appropriate tests and run them::

    $ python setup.py test

In the future there will be CI and more info on contributing.


Contents:

.. toctree::
   :maxdepth: 2

   gremlinrestclient



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Github: https://github.com/davebshow/gremlinrestclient/issues
.. _`pyblueprints`: https://github.com/escalant3/pyblueprints/blob/master/pyblueprints/base.py
