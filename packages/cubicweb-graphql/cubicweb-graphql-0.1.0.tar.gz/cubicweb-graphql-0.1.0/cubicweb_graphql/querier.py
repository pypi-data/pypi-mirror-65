# copyright 2003-2018 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.
"""Implementation of GraphQL support for CubicWeb"""

from gql_schema import create_graphql_schema
from resolver import Resolver, CONNECTION
from graphql.error import format_error as format_graphql_error, GraphQLError
import six


class GraphQLQuerier(object):
    """
    Main entry point for the execution of GraphQL queries
    """

    @staticmethod
    def register(repository):
        """
        Register a repository into this querier
        :param repository: The repository to register
        :return: Nothing
        """
        repository.graphql = _GraphQLQuerierPart(repository, repository.schema)

    @staticmethod
    def execute(connection, query, **kwargs):
        """
        Execute a GraphQL query
        :param connection: The current connection
        :param query: The query to execute
        :param kwargs: The mapping of values for the named variables in the query
        :return: The GraphQL execution result
        """
        return connection.repo.graphql.execute(connection, query, **kwargs)


class _GraphQLQuerierPart(object):
    """
    Part of a GraphQL querier for a specific repository
    """

    def __init__(self, repository, yams_schema):
        """
        Initialize this structure
        :param repository: The parent repository
        :param yams_schema: The input YAMS schema
        """
        # system info helper
        self._repo = repository
        self._resolver = Resolver(repository, yams_schema, lambda: self._query_schema)
        self._query_schema = create_graphql_schema(yams_schema, self._resolver)

    def execute(self, connection, query, **kwargs):
        """
        Execute a GraphQL query
        :param connection: The current connection
        :param query: The query to execute
        :param kwargs: The mapping of values for the named variables in the query
        :return: The GraphQL execution result
        """
        return self._query_schema.execute(query, context={CONNECTION: connection}, values=kwargs)


def default_format_error(error):
    """
    Default formatter for GraphQL errors
    :param error: The error to format
    :return: The formatted error
    """
    if isinstance(error, GraphQLError):
        return format_graphql_error(error)
    return {'message': six.text_type(error)}


def format_execution_result(execution_result, format_error=default_format_error):
    """
    Format a GraphQL execution result for JSON serialization
    :param execution_result: The execution result to format
    :param format_error: The format to use for GraphQL errors
    :return: The formatted execution result
    """
    if execution_result:
        response = {}
        if execution_result.errors:
            response['errors'] = [
                format_error(e) for e in execution_result.errors
            ]
        if not execution_result.invalid:
            response['data'] = execution_result.data
        return response
