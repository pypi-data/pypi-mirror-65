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
"""Implement the interface of a GraphQL schema for YAMS"""

import binascii
import graphene
import graphene.types.datetime
import graphene.relay
from graphql.language import ast
import json

import utils

TYPE_FIELD_META = "_meta"  # Name of the meta field for a GraphQL object type class
_TYPE_FIELD_SCHEMA = "__schema"  # Attribute name for the reference to the YAMS entity schema from a GraphQL object type
FIELD_SUB_SEPARATOR = "_as_"  # Separator between a field name and its type in generated typed sub-fields (e.g. thing_as_Stuff)
_FIELD_CREATE = "create"  # Prefix for the mutation fields for object creators
_FIELD_UPDATE = "update"  # Prefix for the mutation fields for object updaters
_FIELD_DELETE = "delete"  # Prefix for the mutation fields for object removers
_FIELD_DELETE_FROM = "deleteFrom"  # Prefix for the mutation fields for relation removers
ARG_UPDATE_OLD = "old"  # Name of the argument in an updater for the values to be matched
ARG_UPDATE_NEW = "new"  # Name of the argument in an updated for the new value
ARG_DELETE_FROM = "from"  # Name of the argument in a delete relation for the targeted entities
_TYPE_META = "Meta"  # Name for the meta-class of a GraphQL object type
_TYPE_FIELDS = "Fields"  # Suffix for the graphene types of inheritable data
_TYPE_INPUT = "InputOf"  # Prefix for the graphene type for input types
_TYPE_CREATOR = "Create"  # Prefix for the graphene type for creator mutation types
_TYPE_UNION = "Union"  # Prefix for the graphene anonymous union types
_TYPE_QUERY = "Query"  # Suffix for the graphene type for the top query type
_TYPE_MUTATION = "Mutation"  # Suffix for the graphene type for the top mutation type


class ScalarBytes(graphene.Scalar):
    """
    Graphene scalar type for YAMS Bytes
    """

    @staticmethod
    def serialize(value):
        return binascii.hexlify(value)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return binascii.unhexlify(node.value)

    @staticmethod
    def parse_value(value):
        return binascii.unhexlify(value)


class ScalarBigInt(graphene.Scalar):
    """
    Graphene scalar type for YAMS BigInt
    """

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return int(node.value)

    @staticmethod
    def parse_value(value):
        return int(value)


class ScalarDecimal(graphene.Scalar):
    """
    Graphene scalar type for YAMS Decimal
    """

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_literal(node):
        raise NotImplementedError

    @staticmethod
    def parse_value(value):
        raise NotImplementedError


class ScalarInterval(graphene.Scalar):
    """
    Graphene scalar type for YAMS Interval
    """

    @staticmethod
    def serialize(value):
        return str(value)

    @staticmethod
    def parse_literal(node):
        raise NotImplementedError

    @staticmethod
    def parse_value(value):
        raise NotImplementedError


class ScalarJsonb(graphene.Scalar):
    """
    Graphene scalar type for the JsonB type
    """

    @staticmethod
    def serialize(value):
        if isinstance(value, str) or isinstance(value, unicode):
            return json.loads(value)
        return value

    @staticmethod
    def parse_literal(node):
        serialized = utils.serialize_value(node)
        return json.loads(serialized)

    @staticmethod
    def parse_value(value):
        raise NotImplementedError


_PRIMITIVES = {
    "String": graphene.String,
    "Password": graphene.String,
    "Int": graphene.Int,
    "Float": graphene.Float,
    "Boolean": graphene.Boolean,
    "Time": graphene.types.datetime.Time,
    "Date": graphene.types.datetime.Date,
    "Datetime": graphene.types.datetime.DateTime,
    "TZTime": graphene.types.datetime.Time,
    "TZDatetime": graphene.types.datetime.DateTime,
    "Bytes": ScalarBytes,
    "BigInt": ScalarBigInt,
    "Decimal": ScalarDecimal,
    "Interval": ScalarInterval,
    "Jsonb": ScalarJsonb
}


class GraphQLSchemaTypes:
    """
    Repository of GraphQL types for a schema
    """

    def __init__(self, schema, resolver):
        """
        Initializes this structure
        :param schema: The input YAMS schema
        :param resolver: The resolver to use
        """
        self.schema = schema
        self.resolver = resolver
        # Map of YAMS entity names to their GraphQL representation
        self.entities = {}
        # Map of inheritable data structure of fields
        self.blobs = {}
        # The known union types
        self.unions = {}
        # Map of YAMS entity names to their GraphQL input representation
        self.inputs = {}
        # Map of YAMS entity names to their corresponding list of possible arguments
        self.arguments = {}
        # Map of YAMS entity names to their corresponding GraphQL updater mutation types
        self.updaters = {}
        # All known GraphQL types
        self.all_types = []
        # The GraphQL top type for the query
        self.query_type = None
        # The GraphQL top type for the mutation
        self.mutation_type = None
        # The final GraphQL schema
        self.graphql_schema = None
        self._produce()

    def _get_union(self, members):
        """
        Get the union type for the specified types
        :param members: The types (schema entities) in this union
        :return: The corresponding union type
        """
        key = tuple(sorted([member.type for member in members]))
        if self.unions.has_key(key):
            return self.unions[key]
        base_classes = (graphene.Union,)
        common = GraphQLSchemaTypes._get_common_ancestor(members)
        if common is not None and common.type + _TYPE_FIELDS in self.blobs:
            base_classes += (self.blobs[common.type + _TYPE_FIELDS],)
        member_types = tuple([self.entities[member.type] for member in members])
        union_members = {_TYPE_META: type(_TYPE_META, (object,), {"types": member_types})}
        result = type(_TYPE_UNION + str(len(self.unions)), base_classes, union_members)
        self.unions[key] = result
        self.all_types.append(result)
        return result

    @staticmethod
    def _get_common_ancestor(members):
        """
        Get the common ancestor for all the members
        :param members: The types (schema entities) in this union
        :return: The common ancestor, if any
        """
        ancestries = []
        for member in members:
            ancestries.append(GraphQLSchemaTypes._get_ancestry_of(member))
        min_length = min([len(ancestry) for ancestry in ancestries])
        result = None
        for i in range(min_length):
            first = ancestries[0][i]
            for j in range(1, len(ancestries)):
                if ancestries[j][i] != first:
                    return result
            # All the same as first
            result = first
        return result

    @staticmethod
    def _get_ancestry_of(entity):
        """
        Get the ancestry of this entity, beginning from the most abstract and terminating by this entity
        :param entity: The entity
        :return: The ancestry
        """
        ancestors = entity.ancestors()
        result = list(reversed(ancestors))
        result.append(entity)
        return result

    def _get_arguments_union(self, members):
        """
        Get the arguments for a union type
        :param members: The types (schema entities) in this union
        :return: The arguments
        """
        result = {}
        for member in members:
            result.update(self.arguments[member.type])
        return result

    def _create_entity_object_type(self, entity_schema):
        """
        Create a GraphQL object type for a YAMS entity
        :param entity_schema: The schema of a YAMS entity
        :return: Nothing
        """
        fields = {  # Data fields
            _TYPE_FIELD_SCHEMA: entity_schema
        }
        for relation in entity_schema.subject_relations():
            if relation.type == "eid":
                # eid is treated as the identifier
                fields["eid"] = graphene.Field(
                    graphene.ID,
                    name="eid",
                    resolver=lambda instance, info, relation_name=relation.type, resolver=self.resolver, *args, **kwargs:
                    resolver.resolve_primitive_field(instance, relation_name, graphene.ID, info, *args, **kwargs))
            elif relation.final:
                # handle a primitive type
                field_type = relation.objects(entity_schema)[0].type
                if _PRIMITIVES.has_key(field_type):
                    target_type = _PRIMITIVES[field_type]
                    fields[relation.type] = graphene.Field(
                        target_type,
                        name=relation.type,
                        resolver=lambda instance, info, relation_name=relation.type, target_type=target_type, resolver=self.resolver, *args, **kwargs:
                        resolver.resolve_primitive_field(instance, relation_name, target_type, info, *args, **kwargs))
            else:
                # handle a reference to another entity
                objects = relation.objects(entity_schema)
                definition = entity_schema.rdef(relation, role="subject", targettype=objects[0])
                is_multi = definition.cardinality[1] == '+' or definition.cardinality[1] == '*'
                if len(objects) > 1:
                    target_type = lambda objects=objects, data=self: data._get_union(objects)
                    arguments = self._get_arguments_union(objects)
                else:
                    target_type = lambda entities=self.entities, n=objects[0].type: entities[n]
                    arguments = self.arguments[objects[0].type]
                if is_multi:
                    fields[relation.type] = graphene.Field(
                        graphene.List(graphene.NonNull(target_type)),
                        name=relation.type,
                        args=arguments,
                        resolver=lambda instance, info, relation_name=relation.type, target_type=target_type, resolver=self.resolver, *args, **kwargs:
                        resolver.resolve_vector_object_field(instance, relation_name, target_type(), info, *args, **kwargs))
                else:
                    fields[relation.type] = graphene.Field(
                        target_type,
                        name=relation.type,
                        args=arguments,
                        resolver=lambda instance, info, relation_name=relation.type, target_type=target_type, resolver=self.resolver, *args, **kwargs:
                        resolver.resolve_scalar_object_field(instance, relation_name, target_type(), info, *args, **kwargs))

        super_entity = entity_schema.specializes()
        sub_entities = entity_schema.specialized_by()
        if len(sub_entities) > 0:
            # Produce a EntityFields graphene AbstractType and a graph ObjectType that inherits from it
            fields[TYPE_FIELD_META] = type(_TYPE_META, (object,), {"name": entity_schema.type + _TYPE_FIELDS})
            if super_entity is not None:
                # Intermediate entity (is a specialization and can be specialized)
                super_type_fields = self.blobs[super_entity.type + _TYPE_FIELDS] if super_entity is not None else None
                class_fields = type(entity_schema.type + _TYPE_FIELDS, (super_type_fields,), fields)
            else:
                # Can be specialized, but is not a specialization
                class_fields = type(entity_schema.type + _TYPE_FIELDS, (object,), fields)
            class_entity = type(entity_schema.type, (graphene.ObjectType, class_fields), {})
            self.blobs[class_fields.__name__] = class_fields
            self.entities[class_entity.__name__] = class_entity
            self.all_types.append(class_entity)
        elif super_entity is not None:
            # This is a specialized entity
            super_type_fields = self.blobs[super_entity.type + _TYPE_FIELDS] if super_entity is not None else None
            class_entity = type(entity_schema.type, (graphene.ObjectType, super_type_fields,), fields)
            self.entities[class_entity.__name__] = class_entity
            self.all_types.append(class_entity)
        else:
            # This entity is not a specialization, nor is it specialized
            class_entity = type(entity_schema.type, (graphene.ObjectType,), fields)
            self.entities[class_entity.__name__] = class_entity
            self.all_types.append(class_entity)

    def _create_entity_input_type(self, entity_schema):
        """
        Create the GraphQL input type for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: Nothing
        """
        fields = {  # Data fields
            _TYPE_FIELD_SCHEMA: entity_schema
        }
        for relation in entity_schema.subject_relations():
            if relation.type == "eid":
                # eid is treated as the identifier
                fields["eid"] = graphene.Field(
                    graphene.ID,
                    name="eid")
            elif relation.final:
                # handle a primitive type
                field_type = relation.objects(entity_schema)[0].type
                if _PRIMITIVES.has_key(field_type):
                    target_type = _PRIMITIVES[field_type]
                    fields[relation.type] = graphene.Field(
                        target_type,
                        name=relation.type)
            else:
                # handle a reference to another entity
                objects = relation.objects(entity_schema)
                if len(objects) > 1:
                    for target_schema in objects:
                        target_type = lambda inputs=self.inputs, n=_TYPE_INPUT + target_schema.type: inputs[n]
                        name = relation.type + FIELD_SUB_SEPARATOR + target_schema.type
                        fields[name] = graphene.Field(
                            target_type,
                            name=name)
                else:
                    target_type = lambda inputs=self.inputs, n=_TYPE_INPUT + objects[0].type: inputs[n]
                    fields[relation.type] = graphene.Field(
                        target_type,
                        name=relation.type)
        class_entity = type(_TYPE_INPUT + entity_schema.type, (graphene.InputObjectType,), fields)
        self.inputs[class_entity.__name__] = class_entity
        self.all_types.append(class_entity)

    def _create_entity_arguments(self, entity_schema):
        """
        Create the GraphQL argument for an input of the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: Nothing
        """
        arguments = {}
        for relation in entity_schema.subject_relations():
            if relation.type == "eid":
                # eid is treated as the identifier
                arguments["eid"] = graphene.Argument(
                    graphene.ID,
                    name="eid",
                    required=False)
            elif relation.final:
                # handle a primitive type
                field_type = relation.objects(entity_schema)[0].type
                if _PRIMITIVES.has_key(field_type):
                    target_type = _PRIMITIVES[field_type]
                    arguments[relation.type] = graphene.Argument(
                        target_type,
                        name=relation.type,
                        required=False)
            else:
                # handle a reference to another entity
                objects = relation.objects(entity_schema)
                if len(objects) > 1:
                    for target_schema in objects:
                        name = relation.type + FIELD_SUB_SEPARATOR + target_schema.type
                        target_type = lambda inputs=self.inputs, n=_TYPE_INPUT + target_schema.type: inputs[n]
                        arguments[name] = graphene.Argument(
                            target_type,
                            name=name,
                            required=False)
                else:
                    target_type = lambda inputs=self.inputs, n=_TYPE_INPUT + objects[0].type: inputs[n]
                    arguments[relation.type] = graphene.Argument(
                        target_type,
                        name=relation.type,
                        required=False)
        self.arguments[entity_schema.type] = arguments

    def _create_entity_query_field(self, entity_schema):
        """
        Create the GraphQL field for the query for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: The corresponding field
        """
        entity_class = self.entities[entity_schema.type]
        return graphene.Field(
            graphene.List(graphene.NonNull(entity_class)),
            name=entity_schema.type,
            args=self.arguments[entity_schema.type],
            resolver=lambda self, info, entity_type=entity_class, resolver=self.resolver, *args, **kwargs:
            resolver.resolve_entities(entity_type, self, info, *args, **kwargs))

    def _create_query_type(self):
        """
        Create the GraphQL query schema
        :return: Nothing
        """
        members = {}
        for entity in self.schema.entities():
            if entity.final:
                continue
            members[entity.type] = self._create_entity_query_field(entity)
        self.query_type = type(self.schema.name + _TYPE_QUERY, (graphene.ObjectType,), members)

    def _create_entity_creator_field(self, entity_schema):
        """
        Create the GraphQL field for the creation mutation for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: The corresponding field
        """
        entity_class = self.entities[entity_schema.type]
        return graphene.Field(
            graphene.NonNull(entity_class),
            name=_FIELD_CREATE + entity_schema.type,
            args=self.arguments[entity_schema.type],
            resolver=lambda self, info, entity_type=entity_class, resolver=self.resolver, *args, **kwargs:
            resolver.on_create_entity(self, info, entity_type, **kwargs))

    def _create_entity_updater_field(self, entity_schema):
        """
        Create the GraphQL field for the update mutation for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: The corresponding field
        """
        entity_class = self.entities[entity_schema.type]
        arguments = {
            ARG_UPDATE_OLD: graphene.Argument(
                self.inputs[_TYPE_INPUT + entity_schema.type],
                name=ARG_UPDATE_OLD,
                required=False
            ),
            ARG_UPDATE_NEW: graphene.Argument(
                self.inputs[_TYPE_INPUT + entity_schema.type],
                name=ARG_UPDATE_NEW,
                required=False
            )
        }
        return graphene.Field(
            graphene.List(graphene.NonNull(entity_class)),
            name=_FIELD_UPDATE + entity_schema.type,
            args=arguments,
            resolver=lambda self, info, entity_type=entity_class, resolver=self.resolver, *args, **kwargs:
            resolver.on_update_entity(self, info, entity_type, **kwargs))

    def _create_entity_deleter_field(self, entity_schema):
        """
        Create the GraphQL field for the removal mutation for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: The corresponding field
        """
        entity_class = self.entities[entity_schema.type]
        return graphene.Field(
            graphene.List(graphene.ID),
            name=_FIELD_DELETE + entity_schema.type,
            args=self.arguments[entity_schema.type],
            resolver=lambda self, info, entity_type=entity_class, resolver=self.resolver, *args, **kwargs:
            resolver.on_delete_entity(self, info, entity_type, **kwargs))

    def _create_entity_relation_deleter_field(self, entity_schema):
        """
        Create the GraphQL field for the removal mutation for the specified entity
        :param entity_schema: The schema of a YAMS entity
        :return: The corresponding field
        """
        entity_class = self.entities[entity_schema.type]
        arguments = {
            ARG_DELETE_FROM: graphene.Argument(
                self.inputs[_TYPE_INPUT + entity_schema.type],
                name=ARG_DELETE_FROM,
                required=False
            ),
        }
        for name, arg in self.arguments[entity_schema.type].items():
            arg_type = arg.type
            if name == "eid" or arg_type in _PRIMITIVES.values():
                # primitive field
                continue
            arguments[name] = arg
        return graphene.Field(
            graphene.List(graphene.ID),
            name=_FIELD_DELETE_FROM + entity_schema.type,
            args=arguments,
            resolver=lambda self, info, entity_type=entity_class, resolver=self.resolver, *args, **kwargs:
            resolver.on_delete_relation(self, info, entity_type, **kwargs))

    def _create_mutation_type(self):
        """
        Create the GraphQL mutation schema
        :return: Nothing
        """
        members = {}
        for entity in self.schema.entities():
            if entity.final:
                continue
            members[_FIELD_CREATE + entity.type] = self._create_entity_creator_field(entity)
            members[_FIELD_UPDATE + entity.type] = self._create_entity_updater_field(entity)
            members[_FIELD_DELETE + entity.type] = self._create_entity_deleter_field(entity)
            members[_FIELD_DELETE_FROM + entity.type] = self._create_entity_relation_deleter_field(entity)
        self.mutation_type = type(self.schema.name + _TYPE_MUTATION, (graphene.ObjectType,), members)

    def _produce(self):
        """
        Create the Graphene schema for the specified YAMS schema
        :return: The corresponding GraphQL query and mutation schemas
        """
        for entity in self.schema.entities():
            if not entity.final:
                self._create_entity_input_type(entity)
                self._create_entity_arguments(entity)

        yams_types = [entity for entity in self.schema.entities() if not entity.final]
        remainings = yams_types
        while len(remainings) > 0:
            yams_types = remainings
            remainings = []
            for entity in yams_types:
                specialization_of = entity.specializes()
                if specialization_of is None or specialization_of.type in self.entities:
                    # We can resolve this type
                    self._create_entity_object_type(entity)
                else:
                    # Cannot resolve yet => wait for the super-type
                    remainings.append(entity)
        self._create_query_type()
        self._create_mutation_type()
        self.graphql_schema = graphene.Schema(query=self.query_type, mutation=self.mutation_type, auto_camelcase=False, types=self.all_types)


def create_graphql_schema(schema, resolver):
    """
    Create the Graphene schema for the specified YAMS schema
    :param schema: The YAMS schema
    :param resolver: The resolver to be used
    :return: The corresponding GraphQL schema
    """
    factory = GraphQLSchemaTypes(schema, resolver)
    return factory.graphql_schema
