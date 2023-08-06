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

"""Utility APIs for the manipulation of GraphQL data types"""

from graphql.language import ast


def serialize_value(value):
    """
    Serializes an instance of graphql.language.ast.Value as a valid JSON string
    :param value: The value to serialize
    :return: The string of a valid JSON representation
    """
    if value is None:
        return "null"
    if isinstance(value, ast.StringValue):
        return '"' + value.value.replace('"', '\\"') + '"'
    elif isinstance(value, ast.IntValue):
        return str(value.value)
    elif isinstance(value, ast.FloatValue):
        return str(value.value)
    elif isinstance(value, ast.BooleanValue):
        return str(value.value)
    elif isinstance(value, ast.Variable):
        raise NotImplementedError
    elif isinstance(value, ast.EnumValue):
        raise NotImplementedError
    elif isinstance(value, ast.ListValue):
        return "[" + ", ".join([serialize_value(x) for x in value.values]) + "]"
    elif isinstance(value, ast.ObjectValue):
        return "{" + ", ".join(
            ["\"" + field.name.value + "\": " + serialize_value(field.value) for field in value.fields]) + "}"
    else:
        raise NotImplementedError
