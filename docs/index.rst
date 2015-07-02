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

- A higher-level class :py:class:`GraphDatabase<gremlinrestclient.client.GraphDatabase>` that provides and object oriented API for creating and accessing nodes and edges.


Releases
========
The latest release of :py:mod:`gremlinrestclient` is **0.0.1**.


Requirements
============

- Python 2.7-3.4
- Tinkerpop 3 Gremlin Server 3.0.0.M9


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
    >>> resp = client.execute("1 + 1")
    >>> resp
    Response(status_code=200, data=[2], message={}, metadata=u'')

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
