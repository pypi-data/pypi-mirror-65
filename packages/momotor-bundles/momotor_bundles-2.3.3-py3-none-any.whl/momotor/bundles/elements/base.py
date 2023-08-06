import typing
from abc import ABC
from pathlib import PurePosixPath

from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.exception import BundleFormatError

__all__ = ['Element', 'NestedElement', 'IdMixin']


ET = typing.TypeVar('ET', bound="Element")
CT = typing.TypeVar('CT', bound=complexTypeDefinition)
PCT = typing.TypeVar('PCT', bound=complexTypeDefinition)


class Element(ABC, typing.Generic[CT]):
    """ Abstract base class for all elements of a Bundle

    :param bundle: The :py:class:`~momotor.bundles.Bundle` containing this element
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        from momotor.bundles.base import Bundle
        assert isinstance(bundle, Bundle)

        self.bundle = bundle

    def create(self: ET, **kwargs) -> ET:
        """ Set this element's attributes

        Usage:

        .. code-block:: python

           element = Element(bundle).create(...)

        :return: self
        """
        raise NotImplementedError

    def recreate(self: ET, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> ET:
        """ Recreate this element in a target bundle

        :param target_bundle: The target bundle
        :type target_bundle: :py:class:`~momotor.bundles.Bundle`
        :param target_basesrc: The base src of the target
        """
        raise NotImplementedError

    @classmethod
    def recreate_list(cls: ET,
                      elements: typing.Optional[typing.Iterator[ET]],
                      target_bundle: "momotor.bundles.Bundle",
                      target_basesrc: PurePosixPath = None,
                      filter: typing.Callable[[ET], bool] = None) -> typing.Optional[typing.List[ET]]:
        """ Recreate a list of elements

        :param elements: List of elements to recreate (can be None)
        :param target_bundle: The target bundle
        :type target_bundle: :py:class:`~momotor.bundles.Bundle`
        :param target_basesrc: The base src of the target
        :param filter: An optional callable to filter the list of elements before recreation. The callable receives
                       an element and should return a boolean
        :return: a list of elements or None if `elements` param was None
        """
        if elements is not None:
            if filter:
                return [element.recreate(target_bundle, target_basesrc) for element in elements if filter(element)]
            else:
                return [element.recreate(target_bundle, target_basesrc) for element in elements]

        return None

    def _create_from_node(self: ET, node: CT) -> ET:
        """ Set this element's attributes from an XML dom node

        :param node: XML dom node
        :return: self
        """
        raise NotImplementedError

    def _construct_node(self) -> CT:
        """ Create a complex type definition from this element """
        raise NotImplementedError

    @staticmethod
    def _check_node_type(node: complexTypeDefinition,
                         expected_type: typing.Type[complexTypeDefinition],
                         allow_none: bool = False):
        """ Check that node has the expected type. Throws :py:exc:`~momotor.bundles.BundleFormatError` if not

        :param node: The node to check
        :param expected_type: The expected type of the node
        :param allow_none: Allow node to be None
        """
        if allow_none and node is None:
            return

        if not isinstance(node, expected_type):
            raise BundleFormatError("Unexpected node type {}, expected {}"
                                    .format(node.__class__.__name__, expected_type.__name__))


# noinspection PyMethodOverriding
class NestedElement(Element[CT], ABC, typing.Generic[CT, PCT]):
    """ Abstract base class for an elements of a Bundle that's nested and has one or two parents, eg:

    .. code-block:: xml

       <options basename="1">
         <option name="2">
       <options>

       <options basename="3">
         <option ref="2">
       </options>

    The option in the first options list has one parent, with basename 1,
    the option in the second options list has two parents, with basenames 1 and 3

    The full name for the first option will be 1.2,
    the full name for the second option will be 1.3.2

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    @typing.overload
    def _create_from_node(self: ET, node: CT, direct_parent: PCT) -> ET:
        ...

    def _create_from_node(self: ET, node: CT, direct_parent: PCT, ref_parent: PCT = None) -> ET:
        """ Set this element's attributes from an XML dom node

        :param node: XML dom node
        :param direct_parent: The XML dom node's direct parent
        :param ref_parent: The XML dom node's ref parent (optional)
        :return: self
        """
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def _get_attr_base_parts(self, attr: str, node: CT, direct_parent: PCT, ref_parent: typing.Optional[PCT],
                             preprocess: typing.Callable[[str], str] = None, *,
                             base_attr: str = None,
                             allow_base_only=False) -> typing.Optional[typing.Tuple]:
        parts = []
        value = getattr(node, attr, None)
        if value is not None or allow_base_only:
            if preprocess is None:
                preprocess = lambda x: x

            if base_attr is None:
                base_attr = f'base{attr}'

            parent_value = getattr(direct_parent, base_attr, None)
            if parent_value is not None:
                parts.append(preprocess(parent_value))

            if ref_parent:
                ref_value = getattr(ref_parent, base_attr, None)
                if ref_value is not None:
                    parts.append(preprocess(ref_value))

            if value is not None:
                parts.append(preprocess(value))

        return tuple(parts) if parts else None


class IdMixin:
    def __init__(self):
        self._id = None

    @property
    def id(self) -> typing.Optional[str]:
        """ The `id` attribute """
        return self._id

    # noinspection PyShadowingBuiltins
    @id.setter
    def id(self, id: typing.Optional[str]):
        assert id is None or isinstance(id, str)
        self._id = id
