import typing

from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.exception import InvalidRefError
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['resolve_ref']


def resolve_ref(tag_name, node, groups: typing.Iterable[typing.Iterable[complexTypeDefinition]]):
    ref = node.ref
    if not ref:
        return None, node

    for group in groups:
        if group:
            for parent in group:
                for name, ref_node in get_nested_complex_nodes(parent, tag_name):
                    if ref_node.id == node.ref:
                        return parent, ref_node

    raise InvalidRefError("Unable to find {} id={}".format(tag_name, ref))
