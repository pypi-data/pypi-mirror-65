import collections
import typing

from pyxb.binding.basis import complexTypeDefinition

__all__ = ['WildcardAttrsMixin']


CT = typing.TypeVar('CT', bound=complexTypeDefinition)


class WildcardAttrsMixin(typing.Generic[CT]):
    def __init__(self):
        self._attrs: typing.Dict[str, str] = {}

    @property
    def attrs(self) -> typing.Dict[str, str]:
        """ Wildcard attributes """
        return self._attrs

    @attrs.setter
    def attrs(self, attrs: typing.Mapping[str, str]):
        assert attrs is None or isinstance(attrs, collections.abc.Mapping)
        self._attrs = {**attrs} if attrs else {}

    def _create_attrs_from_node(self, node: CT):
        self._attrs = {
            str(key): value
            for key, value in node.wildcardAttributeMap().items()
        }

    def _construct_attrs(self, node: CT) -> CT:
        for key, value in self._attrs.items():
            node._setAttribute(key, value)

        return node
