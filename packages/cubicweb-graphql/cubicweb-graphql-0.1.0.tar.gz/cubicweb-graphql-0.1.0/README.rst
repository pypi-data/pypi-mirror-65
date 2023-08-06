===================
cubicweb-graphql
===================

`cubicweb-graphql`_ provides a `GraphQL`_ interface and querier for CubicWeb.

.. _`GraphQL`: \
    https://graphql.org/


Basic use in Python
-------------------

Once the CubicWeb instance has been launched, GraphQL queries can be executed using:

::

    from cubicweb_graphql.querier import GraphQLQuerier

    query = "query getAffaire($affaire_eid: ID) { Affaire(eid: $affaire_eid) { sujet } }"
    result = GraphQLQuerier.execute(connection, query, affaire_eid=self.affaire1)


Access from the Web API
-----------------------

The GraphQL querier can be access through the Web API:

::

    curl "http://localhost:8080/ajax" \
            -d "fname=graphql" \
            -d "query=$QUERY" \

.

Testing
-------

Tests can be run using:

::

    python -m unittest discover -s test

from top-level directory.