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
"""Implement the resolver for CubicWeb entities"""
from gql_schema import FIELD_SUB_SEPARATOR, TYPE_FIELD_META, ARG_UPDATE_OLD, ARG_UPDATE_NEW, ARG_DELETE_FROM

CONNECTION = "__connection"  # The key for the current connection in the context of a GraphQL query
_CACHE = "__cache"  # The key for the object cache in the context of a GraphQL query
_MODEL = "__model"  # The attribute name that refers to the CubicWeb entity from the GraphQL object instance
_SUBJECT_ARG = "_subject"  # argument name for the current subject of a query
_ARG_PREFIX = "arg"  # Prefix for generated query arguments
_SUBJECT_VAR = "X"  # Name of the first subject in generated RQL queries


class Resolver:
    """The resolver is in charge of fetching the backing data for the GraphQL query execution engine"""

    def __init__(self, repository, yams_schema, graphql_schema):
        """
        Initialize the resolver
        :param repository: The parent repository
        :param yams_schema: The current YAMS schema
        :param graphql_schema: The corresponding GraphQL schema
        """
        self._repository = repository
        self._yams_schema = yams_schema
        self._graphql_schema = graphql_schema

    def get_yams_schema(self):
        """
        Get the associated YAMS schema
        :return: The associated YAMS schema
        """
        if callable(self._yams_schema):
            return self._yams_schema()
        return self._yams_schema

    def get_query_schema(self):
        """
        Get the associated GraphQL query schema
        :return: The associated GraphQL query schema
        """
        if callable(self._graphql_schema):
            return self._graphql_schema()
        return self._graphql_schema

    def _resolve_entity(self, cache, entity):
        """
        Resolve the GraphQL instance object for the specified entity
        :param cache: The cache of GraphQL instances for the current query
        :param entity: The YAMS object instance
        :return: The GraphQL instance object
        """
        type_name = type(entity).__name__
        graphql_type = self.get_query_schema().get_type(type_name).graphene_type
        return Resolver._get_graphql_entity(cache, graphql_type, entity)

    @staticmethod
    def _resolve_entity_from_eid(cache, entity_type, connection, eid):
        """
        Resolve the GraphQL instance object for the specified entity EID
        :param cache: The cache of GraphQL instances for the current query
        :param entity_type: The GraphQL object type to instantiate for the entity
        :param connection: The current connection
        :param eid: The EID of the object to retrieve
        :return: The GraphQL instance object
        """
        try:
            entity = connection.entity_cache(eid)
        except KeyError:
            entity = connection.vreg['etypes'].etype_class(entity_type.__name__)(connection)
            entity.eid = eid
            connection.set_entity_cache(entity)
        return Resolver._get_graphql_entity(cache, entity_type, entity)

    @staticmethod
    def _get_graphql_entity(cache, entity_type, entity):
        """
        Resolve the GraphQL instance object for the specified entity
        :param cache: The cache of GraphQL instances for the current query
        :param entity_type: The GraphQL object type to instantiate for the entity
        :param entity: The YAMS object instance
        :return: The GraphQL instance object
        """
        result = cache.get(entity, None)
        if result is None:
            result = entity_type()
            setattr(result, _MODEL, entity)
            cache[entity] = result
        return result

    @staticmethod
    def _get_cache_for(info):
        """
        Get the GraphQL object instance cache for the specified query info
        :param info: Some complementary GraphQL information
        :return: The GraphQL object instance cache
        """
        result = info.context.get(_CACHE, None)
        if result is None:
            result = {}
            info.context[_CACHE] = result
        return result

    @staticmethod
    def _get_constraints(subject, arguments):
        """
        Get the constraints to be applied to the subject of a query
        :param subject: The subject of the constraints
        :param arguments: The input GraphQL query arguments
        :return: A tuple of the RQL constraints and new arguments
        """
        constraints = []
        new_arguments = {}
        Resolver._build_constraints(subject, arguments, constraints, new_arguments)
        return constraints, new_arguments

    @staticmethod
    def _build_constraints(subject, restrictions, constraints, new_arguments, sub_start=0):
        """
        Build the set of constraints applicable for a RQL query
        :param subject: The subject of the constraints
        :param restrictions: The restrictions to be applied on the subject
        :param constraints: The buffer of resulting constraints
        :param new_arguments: The map of resulting arguments
        :param sub_start: Starting index of the generated sub variables for the specified subject
        :return: The new index of the generated sub variables for the specified subject
        """
        sub = sub_start
        for field, value in restrictions.items():
            if FIELD_SUB_SEPARATOR in field:
                field = field[0:field.index(FIELD_SUB_SEPARATOR)]
            if hasattr(value, TYPE_FIELD_META):
                # this is a complex value
                sub_restrictions = {k: v for k, v in value.__dict__.items() if not k.startswith("_") and v is not None}
                sub_subject = subject + str(chr(ord('A') + sub))
                sub += 1
                constraints.append(subject + " " + field + " " + sub_subject)
                Resolver._build_constraints(sub_subject, sub_restrictions, constraints, new_arguments)
            else:
                # simple value
                arg_name = _ARG_PREFIX + str(len(new_arguments))
                constraints.append(subject + " " + field + " %(" + arg_name + ")s")
                new_arguments[arg_name] = value
        return sub

    def resolve_entities(self, entity_type, query, info, *args, **kwargs):
        """
        Fetch entities of the specified type
        :param entity_type: The GraphQL Object Type for the entity
        :param query: The GraphQL being resolved
        :param info: Some complementary GraphQL information
        :param args: The passed arguments
        :param kwargs: The query parameters
        :return: The resolved entities
        """
        connection = info.context[CONNECTION]
        cache = Resolver._get_cache_for(info)
        if kwargs is None or len(kwargs) == 0:
            rql = entity_type.__name__ + " " + _SUBJECT_VAR
            arguments = {}
        else:
            rql = entity_type.__name__ + " " + _SUBJECT_VAR + " WHERE"
            constraints, arguments = Resolver._get_constraints(_SUBJECT_VAR, kwargs)
            first = True
            for constraint in constraints:
                if not first:
                    rql += " AND"
                first = False
                rql += " " + constraint
        results = connection.execute(rql, arguments)
        return [self._get_graphql_entity(cache, entity_type, entity) for entity in results.entities()]

    def resolve_primitive_field(self, instance, relation_name, target_type, info, *args, **kwargs):
        """
        Fetch the values for an entity's field when its type is primitive
        :param instance: The entity's instance
        :param relation_name: The name of the relation for this field
        :param target_type: The GraphQL type for this field
        :param info: Some complementary GraphQL information
        :param args: The passed arguments
        :param kwargs: The query parameters
        :return: The resolved value
        """
        model = getattr(instance, _MODEL)
        return getattr(model, relation_name)

    def resolve_scalar_object_field(self, instance, relation_name, target_type, info, *args, **kwargs):
        """
        Fetch the values for an entity's field when its type is a single instance of an entity
        :param instance: The entity's instance
        :param relation_name: The name of the relation for this field
        :param target_type: The GraphQL type for this field
        :param info: Some complementary GraphQL information
        :param args: The passed arguments
        :param kwargs: The query parameters
        :return: The resolved value
        """
        return self._resolve_object_field(instance, relation_name, target_type, info, True, *args, **kwargs)

    def resolve_vector_object_field(self, instance, relation_name, target_type, info, *args, **kwargs):
        """
        Fetch the values for an entity's field when its type is a collection of instances of other entities
        :param instance: The entity's instance
        :param relation_name: The name of the relation for this field
        :param target_type: The GraphQL type for this field
        :param info: Some complementary GraphQL information
        :param args: The passed arguments
        :param kwargs: The query parameters
        :return: The resolved value
        """
        return self._resolve_object_field(instance, relation_name, target_type, info, False, *args, **kwargs)

    def _resolve_object_field(self, instance, relation_name, target_type, info, scalar, *args, **kwargs):
        """
        Fetch the values for an entity's field when its type is another entity
        :param instance: The entity's instance
        :param relation_name: The name of the relation for this field
        :param target_type: The GraphQL type for this field
        :param info: Some complementary GraphQL information
        :param scalar: Whether this is a scalar field
        :param args: The passed arguments
        :param kwargs: The query parameters
        :return: The resolved value
        """
        model = getattr(instance, _MODEL)
        cache = Resolver._get_cache_for(info)
        if kwargs is None or len(kwargs) == 0:
            if scalar:
                # Get the single value
                value = getattr(model, relation_name)
                if isinstance(value, tuple):
                    value = value[0]
                return self._resolve_entity(cache, value)
            else:
                # Get all the values
                values = getattr(model, relation_name)
                return [self._resolve_entity(cache, x) for x in values]
        else:
            # Generate a RQL query and execute it
            connection = info.context[CONNECTION]
            rql = "Any " + _SUBJECT_VAR + " WHERE S " + relation_name + " " + _SUBJECT_VAR + " AND S eid %(" + _SUBJECT_ARG + ")s"
            constraints, arguments = self._get_constraints(_SUBJECT_VAR, kwargs)
            for constraint in constraints:
                rql += " AND " + constraint
            arguments[_SUBJECT_ARG] = model.eid
            results = connection.execute(rql, arguments)
            values = [self._resolve_entity(cache, entity) for entity in results.entities()]
            if scalar:
                return values[0] if len(values) > 0 else None
            return values

    @staticmethod
    def _get_insertion_rql(type_name, arguments):
        """
        Generate the RQL statement for an insertion
        :param type_name: The name of the type of entity to create
        :param arguments: The arguments for the creation
        :return: A tuple of the RQL statement and its arguments
        """
        fields = []
        constraints = []
        new_arguments = {}
        sub = 0
        for field, value in arguments.items():
            if FIELD_SUB_SEPARATOR in field:
                field = field[0:field.index(FIELD_SUB_SEPARATOR)]
            if hasattr(value, TYPE_FIELD_META):
                # this is a complex value
                sub_restrictions = {k: v for k, v in value.__dict__.items() if not k.startswith("_") and v is not None}
                sub_subject = _SUBJECT_VAR + str(chr(ord('A') + sub))
                sub += 1
                fields.append(_SUBJECT_VAR + " " + field + " " + sub_subject)
                Resolver._build_constraints(sub_subject, sub_restrictions, constraints, new_arguments)
            else:
                # simple value
                arg_name = _ARG_PREFIX + str(len(new_arguments))
                fields.append(_SUBJECT_VAR + " " + field + " %(" + arg_name + ")s")
                new_arguments[arg_name] = value
        rql = "INSERT " + type_name + " " + _SUBJECT_VAR + ":"
        for i in range(len(fields)):
            prefix = ", " if i > 0 else " "
            rql += prefix + fields[i]
        if len(constraints) > 0:
            rql += " WHERE"
            for i in range(len(constraints)):
                prefix = " AND " if i > 0 else " "
                rql += prefix + constraints[i]
        return rql, new_arguments

    def on_create_entity(self, root, info, entity_type, **kwargs):
        """
        Create a new instance of an entity
        :param root: The GraphQL query root
        :param info: Some complementary GraphQL information
        :param entity_type: The GraphQL type to instantiate
        :param kwargs: The query parameters
        :return: The instantiated entity
        """
        rql, arguments = Resolver._get_insertion_rql(entity_type.__name__, kwargs or {})
        connection = info.context[CONNECTION]
        cache = Resolver._get_cache_for(info)
        results = connection.execute(rql, arguments)
        values = [Resolver._get_graphql_entity(cache, entity_type, entity) for entity in results.entities()]
        return values[0] if len(values) > 0 else None

    @staticmethod
    def _get_update_rql(type_name, arguments):
        """
        Generate the RQL statement for an insertion
        :param type_name: The name of the type of entity to update
        :param arguments: The arguments for the creation
        :return: A tuple of the RQL statement and its arguments
        """
        fields = []
        constraints = []
        new_arguments = {}
        sub = 0

        # gather constraints for matching current entities
        sub_restrictions = {k: v for k, v in arguments[ARG_UPDATE_OLD].__dict__.items() if not k.startswith("_") and v is not None}
        sub = Resolver._build_constraints(_SUBJECT_VAR, sub_restrictions, constraints, new_arguments, sub)

        # gather new fields to set for the matched entities
        sub_restrictions = {k: v for k, v in arguments[ARG_UPDATE_NEW].__dict__.items() if not k.startswith("_") and v is not None}
        for field, value in sub_restrictions.items():
            if FIELD_SUB_SEPARATOR in field:
                field = field[0:field.index(FIELD_SUB_SEPARATOR)]
            if hasattr(value, TYPE_FIELD_META):
                # this is a complex value
                value_restrictions = {k: v for k, v in value.__dict__.items() if not k.startswith("_") and v is not None}
                sub_subject = _SUBJECT_VAR + str(chr(ord('A') + sub))
                sub += 1
                fields.append(_SUBJECT_VAR + " " + field + " " + sub_subject)
                Resolver._build_constraints(sub_subject, value_restrictions, constraints, new_arguments)
            else:
                # simple value
                arg_name = _ARG_PREFIX + str(len(new_arguments))
                fields.append(_SUBJECT_VAR + " " + field + " %(" + arg_name + ")s")
                new_arguments[arg_name] = value

        rql = "SET"
        for i in range(len(fields)):
            prefix = ", " if i > 0 else " "
            rql += prefix + fields[i]
        rql += " WHERE " + _SUBJECT_VAR + " is " + type_name
        for constraint in constraints:
            rql += " AND " + constraint
        return rql, new_arguments

    def on_update_entity(self, root, info, entity_type, **kwargs):
        """
        Update instances of an entity
        :param root: The GraphQL query root
        :param info: Some complementary GraphQL information
        :param entity_type: The GraphQL Object Type for the entity
        :param kwargs: The query parameters
        :return: The updated entities
        """
        rql, arguments = Resolver._get_update_rql(entity_type.__name__, kwargs or {})
        connection = info.context[CONNECTION]
        cache = Resolver._get_cache_for(info)
        results = connection.execute(rql, arguments)
        # no description is built for SET queries
        return [self._resolve_entity_from_eid(cache, entity_type, connection, results.rows[i][0]) for i in range(len(results))]

    @staticmethod
    def _get_delete_rql(type_name, arguments):
        """
        Generate the RQL statement for a deletion
        :param type_name: The name of the type of entity to delete
        :param arguments: The arguments for the creation
        :return: A tuple of the RQL statement and its arguments
        """
        constraints, new_arguments = Resolver._get_constraints(_SUBJECT_VAR, arguments)
        rql = "DELETE " + type_name + " " + _SUBJECT_VAR
        for i in range(len(constraints)):
            rql += " WHERE " if i == 0 else " AND "
            rql += constraints[i]
        return rql, new_arguments

    def on_delete_entity(self, root, info, entity_type, **kwargs):
        """
        Delete instances of an entity
        :param root: The GraphQL query root
        :param info: Some complementary GraphQL information
        :param entity_type: The GraphQL Object Type for the entity
        :param kwargs: The query parameters
        :return: The EID of the delete entities
        """
        rql, arguments = Resolver._get_delete_rql(entity_type.__name__, kwargs or {})
        connection = info.context[CONNECTION]
        results = connection.execute(rql, arguments)
        return [row[0] for row in results.rows]

    @staticmethod
    def _get_delete_relation_rql(type_name, arguments):
        """
        Generate the RQL statement for a relation deletion
        :param type_name: The name of the type of source entity
        :param arguments: The arguments for the creation
        :return: A tuple of the RQL statement and its arguments
        """
        constraints = []
        new_arguments = {}
        to_delete = []
        sub = 0
        # gather constraints for matching source entities
        sub_restrictions = {k: v for k, v in arguments[ARG_DELETE_FROM].__dict__.items() if not k.startswith("_") and v is not None}
        sub = Resolver._build_constraints(_SUBJECT_VAR, sub_restrictions, constraints, new_arguments, sub)

        for field, value in arguments.items():
            if field == ARG_DELETE_FROM:
                continue
            if FIELD_SUB_SEPARATOR in field:
                field = field[0:field.index(FIELD_SUB_SEPARATOR)]
            value_restrictions = {k: v for k, v in value.__dict__.items() if not k.startswith("_") and v is not None}
            sub_subject = _SUBJECT_VAR + str(chr(ord('A') + sub))
            sub += 1
            to_delete.append(_SUBJECT_VAR + " " + field + " " + sub_subject)
            Resolver._build_constraints(sub_subject, value_restrictions, constraints, new_arguments)
        rql = "DELETE"
        for i in range(len(to_delete)):
            prefix = ", " if i > 0 else " "
            rql += prefix + to_delete[i]

        rql += " WHERE " + _SUBJECT_VAR + " is " + type_name
        for constraint in constraints:
            rql += " AND " + constraint
        return rql, new_arguments

    def on_delete_relation(self, root, info, entity_type, **kwargs):
        """
        Delete relations between entities
        :param root: The GraphQL query root
        :param info: Some complementary GraphQL information
        :param entity_type: The GraphQL Object Type for the source entity
        :param kwargs: The query parameters
        :return: The EID of the delete relations
        """
        rql, arguments = Resolver._get_delete_relation_rql(entity_type.__name__, kwargs or {})
        connection = info.context[CONNECTION]
        connection.execute(rql, arguments)
        return []
