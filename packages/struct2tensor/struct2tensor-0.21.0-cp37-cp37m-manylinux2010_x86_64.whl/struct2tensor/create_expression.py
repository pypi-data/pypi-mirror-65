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
"""Convert a Prensor to an Expression.

create_expression_from_prensor(...) creates an Expression from a Prensor.

"""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

from struct2tensor import calculate_options
from struct2tensor import expression
from struct2tensor import path
from struct2tensor import prensor
import tensorflow as tf
from typing import FrozenSet, Mapping, Optional, Sequence


class _DirectExpression(expression.Expression):
  """An expression where the value is immediate.

  This expression has no sources, and a NodeTensor is set at construction time.
  """

  def __init__(self, is_repeated: bool, my_type: Optional[tf.DType],
               value: prensor.NodeTensor,
               children: Mapping[path.Step, expression.Expression]):
    """Initializes an expression.

    Args:
      is_repeated: if the expression is repeated.
      my_type: the DType of a field, or None for an internal node.
      value: the return value of calculate(...)
      children: the subexpressions.
    """
    super(_DirectExpression, self).__init__(is_repeated, my_type)
    self._value = value
    self._children = children

  def get_source_expressions(self) -> Sequence[expression.Expression]:
    return []

  def calculate(
      self,
      sources: Sequence[prensor.NodeTensor],
      destinations: Sequence[expression.Expression],
      options: calculate_options.Options,
      side_info: Optional[prensor.Prensor] = None) -> prensor.NodeTensor:
    return self._value

  def calculation_is_identity(self) -> bool:
    return False

  def calculation_equal(self, expr: expression.Expression) -> bool:
    return isinstance(expr, _DirectExpression) and expr._value is self._value  # pylint: disable=protected-access

  def _get_child_impl(self,
                      field_name: path.Step) -> Optional[expression.Expression]:
    return self._children.get(field_name)

  def known_field_names(self) -> FrozenSet[path.Step]:
    return frozenset(self._children.keys())

  def __str__(self) -> str:  # pylint: disable=g-ambiguous-str-annotation
    return "_DirectExpression: {}".format(str(id(self)))


def create_expression_from_prensor(t: prensor.Prensor) -> expression.Expression:
  """Gets an expression representing the prensor.

  Args:
    t: The prensor to represent.

  Returns:
    An expression representing the prensor.
  """
  node_tensor = t.node
  children = {
      k: create_expression_from_prensor(v) for k, v in t.get_children().items()
  }
  if isinstance(node_tensor, prensor.RootNodeTensor):
    return _DirectExpression(True, None, node_tensor, children)
  elif isinstance(node_tensor, prensor.ChildNodeTensor):
    return _DirectExpression(node_tensor.is_repeated, None, node_tensor,
                             children)
  else:
    # isinstance(node_tensor, LeafNodeTensor)
    return _DirectExpression(node_tensor.is_repeated, node_tensor.values.dtype,
                             node_tensor, children)
