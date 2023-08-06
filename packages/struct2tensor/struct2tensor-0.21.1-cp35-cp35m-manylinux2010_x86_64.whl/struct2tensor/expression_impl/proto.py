# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Expressions to parse a proto.

These expressions return values with more information than standard node values.
Specifically, each node calculates additional tensors that are used as inputs
for its children.
"""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function


import abc
from struct2tensor import calculate_options
from struct2tensor import expression
from struct2tensor import path
from struct2tensor import prensor
from struct2tensor.expression_impl import parse_message_level_ex
from struct2tensor.ops import struct2tensor_ops
import tensorflow as tf
from typing import FrozenSet, Mapping, Optional, Sequence, Set, Text, Tuple, Union


from google.protobuf.descriptor_pb2 import FileDescriptorSet
from google.protobuf import descriptor
from google.protobuf.descriptor_pool import DescriptorPool

# To the best of my knowledge, ProtoFieldNames ARE strings.
# Also includes extensions, encoded in a parentheses like (foo.bar.Baz).
ProtoFieldName = str  # pylint: disable=g-ambiguous-str-annotation
ProtoFullName = str  # pylint: disable=g-ambiguous-str-annotation

# A string representing a step in a path.
StrStep = str  # pylint: disable=g-ambiguous-str-annotation


def is_proto_expression(expr: expression.Expression) -> bool:
  """Returns true if an expression is a ProtoExpression."""
  return isinstance(
      expr, (_ProtoRootExpression, _ProtoChildExpression, _ProtoLeafExpression))


def create_expression_from_file_descriptor_set(
    tensor_of_protos: tf.Tensor,
    proto_name: ProtoFullName,
    file_descriptor_set: FileDescriptorSet,
    message_format: Text = "binary") -> expression.Expression:
  """Create an expression from a 1D tensor of serialized protos.

  Args:
    tensor_of_protos: 1D tensor of serialized protos.
    proto_name: fully qualified name (e.g. "some.package.SomeProto") of the
      proto in `tensor_of_protos`.
    file_descriptor_set: The FileDescriptorSet proto containing `proto_name`'s
      and all its dependencies' FileDescriptorProto. Note that if file1 imports
      file2, then file2's FileDescriptorProto must precede file1's in
      file_descriptor_set.file.
    message_format: Indicates the format of the protocol buffer: is one of
       'text' or 'binary'.

  Returns:
    An expression.
  """

  pool = DescriptorPool()
  for f in file_descriptor_set.file:
    # This method raises if f's dependencies have not been added.
    pool.Add(f)

  # This method raises if proto not found.
  desc = pool.FindMessageTypeByName(proto_name)

  return create_expression_from_proto(tensor_of_protos, desc, message_format)


def create_expression_from_proto(
    tensor_of_protos: tf.Tensor,
    desc: descriptor.Descriptor,
    message_format: Text = "binary") -> expression.Expression:
  """Create an expression from a 1D tensor of serialized protos.

  Args:
    tensor_of_protos: 1D tensor of serialized protos.
    desc: a descriptor of protos in tensor of protos.
    message_format: Indicates the format of the protocol buffer: is one of
      'text' or 'binary'.

  Returns:
    An expression.
  """
  return _ProtoRootExpression(desc, tensor_of_protos, message_format)


class _ProtoRootNodeTensor(prensor.RootNodeTensor):
  """The value of the root node.

  This not only contains the normal size information, but also information
  needed by its children.

  In particular:
  1. Any needed regular fields are included.
  2. Any needed extended fields are included.
  3. Any needed map fields are included.
  4. if this is an Any proto, any needed casted fields are included.

  """

  def __init__(self, size: tf.Tensor,
               fields: Mapping[StrStep, struct2tensor_ops._ParsedField]):
    super(_ProtoRootNodeTensor, self).__init__(size)
    self.fields = fields


class _ProtoChildNodeTensor(prensor.ChildNodeTensor):
  """The value of a child node.

  This not only contains the normal parent_index information, but also
  information needed by its children.

  In particular:
  1. Any needed regular fields are included.
  2. Any needed extended fields are included.
  3. Any needed map fields are included.
  4. if this is an Any proto, any needed casted fields are included.
  """

  def __init__(self, parent_index: tf.Tensor, is_repeated: bool,
               fields: Mapping[StrStep, struct2tensor_ops._ParsedField]):
    super(_ProtoChildNodeTensor, self).__init__(parent_index, is_repeated)
    self.fields = fields


_ParentProtoNodeTensor = Union[_ProtoRootNodeTensor, _ProtoChildNodeTensor]


class _AbstractProtoChildExpression(expression.Expression):
  """A child or leaf proto expression."""

  def __init__(self, parent: "_ParentProtoExpression", name_as_field: StrStep,
               is_repeated: bool, my_type: Optional[tf.DType]):
    super(_AbstractProtoChildExpression, self).__init__(is_repeated, my_type)
    self._parent = parent
    self._name_as_field = name_as_field

  @property
  def name_as_field(self) -> StrStep:
    return self._name_as_field

  def get_needed_fields(self, expr: expression.Expression) -> Sequence[StrStep]:
    return [self._name_as_field]

  def get_path(self) -> path.Path:
    """Returns the path to the root of the proto."""
    return self._parent.get_path().get_child(self.name_as_field)

  def get_proto_source(self) -> Tuple[tf.Tensor, descriptor.Descriptor]:
    """Returns the proto root."""
    return self._parent.get_proto_source()

  def get_source_expressions(self) -> Sequence[expression.Expression]:
    # In order to parse this proto, you need to parse its parent.
    return [self._parent]

  def calculate(
      self,
      sources: Sequence[prensor.NodeTensor],
      destinations: Sequence[expression.Expression],
      options: calculate_options.Options,
      side_info: Optional[prensor.Prensor] = None) -> prensor.NodeTensor:
    [parent_value] = sources
    if isinstance(parent_value, _ProtoRootNodeTensor) or isinstance(
        parent_value, _ProtoChildNodeTensor):
      parsed_field = parent_value.fields.get(self.name_as_field)
      if parsed_field is None:
        raise ValueError("Cannot find {} in {}".format(
            str(self), str(parent_value)))
      return self.calculate_from_parsed_field(parsed_field, destinations)
    raise ValueError("Not a _ParentProtoNodeTensor: " + str(type(parent_value)))

  @abc.abstractmethod
  def calculate_from_parsed_field(self,
                                  parsed_field: struct2tensor_ops._ParsedField,
                                  destinations: Sequence[expression.Expression]
                                 ) -> prensor.NodeTensor:
    """Calculate the NodeTensor given the parsed fields requested from a parent.

    Args:
      parsed_field: the parsed field from name_as_field.
      destinations: the destination of the expression.
    Returns:
      A node tensor for this node.
    """
    raise NotImplementedError()

  def calculation_is_identity(self) -> bool:
    return False


class _ProtoLeafExpression(_AbstractProtoChildExpression):
  """Represents parsing a leaf field."""

  def __init__(self, parent: "_ParentProtoExpression",
               desc: descriptor.FieldDescriptor, name_as_field: path.Step):
    """Initialize a proto leaf expression.

    Args:
      parent: the parent of the expression.
      desc: the field descriptor of the expression name_as_field.
      name_as_field: the name of the field.
    """
    super(_ProtoLeafExpression, self).__init__(
        parent, name_as_field,
        desc.label == descriptor.FieldDescriptor.LABEL_REPEATED,
        struct2tensor_ops._get_dtype_from_cpp_type(desc.cpp_type))  # pylint: disable=protected-access
    # TODO(martinz): make _get_dtype_from_cpp_type public.
    self._field_descriptor = desc

  def calculate_from_parsed_field(self,
                                  parsed_field: struct2tensor_ops._ParsedField,
                                  destinations: Sequence[expression.Expression]
                                 ) -> prensor.NodeTensor:
    return prensor.LeafNodeTensor(parsed_field.index, parsed_field.value,
                                  self.is_repeated)

  def calculation_equal(self, expr: expression.Expression) -> bool:
    # pylint: disable=protected-access
    return (isinstance(expr, _ProtoLeafExpression) and
            self._field_descriptor == expr._field_descriptor and
            self.name_as_field == expr.name_as_field)

  def _get_child_impl(self,
                      field_name: path.Step) -> Optional[expression.Expression]:
    return None

  def known_field_names(self) -> FrozenSet[path.Step]:
    return frozenset()

  def __str__(self) -> str:  # pylint: disable=g-ambiguous-str-annotation
    return "_ProtoLeafExpression: {} from {}".format(self.name_as_field,
                                                     self._parent)


class _ProtoChildExpression(_AbstractProtoChildExpression):
  """An expression representing a proto submessage.

  Supports:
    A standard submessage.
    An extension submessage.
    A protobuf.Any submessage.
    A proto map submessage.
    Also supports having fields of the above types.
  """

  def __init__(self, parent: "_ParentProtoExpression",
               desc: descriptor.Descriptor, is_repeated: bool,
               name_as_field: StrStep):
    """Initialize a _ProtoChildExpression.

    This does not take a field descriptor so it can represent syntactic sugar
    fields such as Any and Maps.
    Args:
      parent: the parent.
      desc: the message descriptor of the submessage represented by this
        expression.
      is_repeated: whether the field is repeated.
      name_as_field: the name of the field.
    """
    super(_ProtoChildExpression, self).__init__(parent, name_as_field,
                                                is_repeated, None)
    self._desc = desc

  def calculate_from_parsed_field(self,
                                  parsed_field: struct2tensor_ops._ParsedField,
                                  destinations: Sequence[expression.Expression]
                                 ) -> prensor.NodeTensor:
    needed_fields = _get_needed_fields(destinations)
    fields = parse_message_level_ex.parse_message_level_ex(
        parsed_field.value, self._desc, needed_fields)
    return _ProtoChildNodeTensor(parsed_field.index, self.is_repeated, fields)

  def calculation_equal(self, expr: expression.Expression) -> bool:
    return (isinstance(expr, _ProtoChildExpression) and
            self._desc == expr._desc and  # pylint: disable=protected-access
            self.name_as_field == expr.name_as_field)

  def _get_child_impl(self,
                      field_name: path.Step) -> Optional[expression.Expression]:
    return _get_child(self, self._desc, field_name)

  def known_field_names(self) -> FrozenSet[path.Step]:
    return _known_field_names_from_descriptor(self._desc)

  def __str__(self) -> str:  # pylint: disable=g-ambiguous-str-annotation
    return "_ProtoChildExpression: name_as_field: {} desc: {} from {}".format(
        str(self.name_as_field), str(self._desc.full_name), self._parent)


class _ProtoRootExpression(expression.Expression):
  """The expression representing the parse of the root of a proto.

  This class returns a _ProtoRootNodeTensor, that parses out fields for
  _ProtoChildExpression and _ProtoLeafExpression to consume.
  """

  def __init__(self,
               desc: descriptor.Descriptor,
               tensor_of_protos: tf.Tensor,
               message_format: Text = "binary"):
    """Initialize a proto expression.

    Args:
      desc: the descriptor of the expression.
      tensor_of_protos: a 1-D tensor to get the protos from.
      message_format: Indicates the format of the protocol buffer: is one of
       'text' or 'binary'.
    """
    super(_ProtoRootExpression, self).__init__(True, None)
    self._descriptor = desc
    self._tensor_of_protos = tensor_of_protos
    self._message_format = message_format

  def get_path(self) -> path.Path:
    """Returns the path to the root of the proto."""
    return path.Path([])

  def get_proto_source(self) -> Tuple[tf.Tensor, descriptor.Descriptor]:
    """Returns the tensor of protos and the original descriptor."""
    return (self._tensor_of_protos, self._descriptor)

  def get_source_expressions(self) -> Sequence[expression.Expression]:
    return []

  def calculate(
      self,
      sources: Sequence[prensor.NodeTensor],
      destinations: Sequence[expression.Expression],
      options: calculate_options.Options,
      side_info: Optional[prensor.Prensor] = None) -> _ProtoRootNodeTensor:
    if sources:
      raise ValueError("_ProtoRootExpression has no sources")
    size = tf.size(self._tensor_of_protos, out_type=tf.int64)
    needed_fields = _get_needed_fields(destinations)
    fields = parse_message_level_ex.parse_message_level_ex(
        self._tensor_of_protos,
        self._descriptor,
        needed_fields,
        message_format=self._message_format)
    return _ProtoRootNodeTensor(size, fields)

  def calculation_is_identity(self) -> bool:
    return False

  def calculation_equal(self, expr: expression.Expression) -> bool:
    # TODO(martinz): In theory, we could check for the equality of the
    # tensor_of_protos and the descriptors.
    return self is expr

  def _get_child_impl(self,
                      field_name: path.Step) -> Optional[expression.Expression]:
    return _get_child(self, self._descriptor, field_name)

  def known_field_names(self) -> FrozenSet[path.Step]:
    return _known_field_names_from_descriptor(self._descriptor)

  def __str__(self) -> str:  # pylint: disable=g-ambiguous-str-annotation
    return "_ProtoRootExpression: {}".format(str(self._descriptor.full_name))


ProtoExpression = Union[_ProtoRootExpression, _ProtoChildExpression,  # pylint: disable=invalid-name
                        _ProtoLeafExpression]

_ParentProtoExpression = Union[_ProtoChildExpression, _ProtoRootExpression]


def _known_field_names_from_descriptor(
    desc: descriptor.Descriptor) -> FrozenSet[StrStep]:
  return frozenset([field.name for field in desc.fields])


def _get_field_descriptor(
    desc: descriptor.Descriptor,
    field_name: ProtoFieldName) -> Optional[descriptor.FieldDescriptor]:
  if path.is_extension(field_name):
    try:
      return desc.file.pool.FindExtensionByName(
          path.get_raw_extension_name(field_name))
    except KeyError:
      return None
  return desc.fields_by_name.get(field_name)


def _get_any_child(
    parent: Union[_ProtoChildExpression, _ProtoRootExpression],
    desc: descriptor.Descriptor, field_name: ProtoFieldName
) -> Optional[Union[_ProtoLeafExpression, _ProtoChildExpression]]:
  """Gets the child of an any descriptor."""
  if path.is_extension(field_name):
    full_name_child = parse_message_level_ex.get_full_name_from_any_step(
        field_name)
    if full_name_child is None:
      return None
    field_message = desc.file.pool.FindMessageTypeByName(full_name_child)
    return _ProtoChildExpression(parent, field_message, False, field_name)
  else:
    return _get_child_helper(parent, desc.fields_by_name.get(field_name),
                             field_name)


def _is_map_field_desc(field_desc: descriptor.FieldDescriptor) -> bool:
  return (field_desc.message_type and
          field_desc.message_type.GetOptions().map_entry)


def _get_map_child(
    parent: Union[_ProtoChildExpression, _ProtoRootExpression],
    desc: descriptor.Descriptor, field_name: ProtoFieldName
) -> Optional[Union[_ProtoLeafExpression, _ProtoChildExpression]]:
  """Gets the child given a map field."""
  [map_field_name, _] = path.parse_map_indexing_step(field_name)
  map_field_desc = desc.fields_by_name.get(map_field_name)
  if map_field_desc is None:
    return None
  if not _is_map_field_desc(map_field_desc):
    return None
  map_message_desc = map_field_desc.message_type
  if map_message_desc is None:
    # Note: I don't know if this is reachable. Theoretically, _is_map_field_desc
    # should have already returned false.
    return None
  value_field_desc = map_message_desc.fields_by_name.get("value")
  if value_field_desc is None:
    # Note: I don't know if this is reachable. Theoretically, _is_map_field_desc
    # should have already returned false.
    return None
  # This relies on the fact that the value is an optional field.
  return _get_child_helper(parent, value_field_desc, field_name)


def _get_child_helper(
    parent: Union[_ProtoChildExpression, _ProtoRootExpression],
    field_descriptor: Optional[descriptor.FieldDescriptor],
    field_name: ProtoFieldName
) -> Optional[Union[_ProtoChildExpression, _ProtoLeafExpression]]:
  """Helper function for _get_child, _get_any_child, and _get_map_child.

  Note that the field_descriptor.field_name is not necessarily equal to
  field_name, especially if this is called from _get_map_child.

  Args:
    parent: the parent expression
    field_descriptor: the field descriptor of the submessage represented by the
      returned expression, if present. If None, this will just return None.
    field_name: the field name of the _AbstractProtoChildExpression returned.

  Returns:
    An _AbstractProtoChildExpression.
  """
  if field_descriptor is None:
    return None
  field_message = field_descriptor.message_type
  if field_message is None:
    return _ProtoLeafExpression(parent, field_descriptor, field_name)
  return _ProtoChildExpression(
      parent, field_message,
      field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED,
      field_name)


def _get_child(parent: Union[_ProtoChildExpression, _ProtoRootExpression],
               desc: descriptor.Descriptor, field_name: path.Step
              ) -> Optional[Union[_ProtoChildExpression, _ProtoLeafExpression]]:
  """Get a child expression.

  This will get one of the following:
    A regular field.
    An extension.
    An Any filtered by value.
    A map field.

  Args:
    parent: The parent expression.
    desc: The descriptor of the parent.
    field_name: The name of the field.

  Returns:
    The child expression, either a submessage or a leaf.
  """
  if isinstance(field_name, path.AnonymousId):
    return None
  if parse_message_level_ex.is_any_descriptor(desc):
    return _get_any_child(parent, desc, field_name)
  if path.is_map_indexing_step(field_name):
    return _get_map_child(parent, desc, field_name)
  # Works for extensions and regular fields, but not any or map.
  return _get_child_helper(parent, _get_field_descriptor(desc, field_name),
                           field_name)


def _get_needed_fields(
    destinations: Sequence[expression.Expression]) -> Set[StrStep]:
  field_names = set()  # type: Set[StrStep]
  for destination in destinations:
    if isinstance(destination, _AbstractProtoChildExpression):
      field_names.add(destination.name_as_field)
  return field_names
