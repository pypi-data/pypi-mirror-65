import typing
from pathlib import PurePosixPath

from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.binding.momotor import propertyComplexType, propertiesComplexType
from momotor.bundles.elements.content import ContentTypeElement
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['Property', 'PropertiesMixin']


class Property(
    ContentTypeElement[propertyComplexType, propertiesComplexType],
    WildcardAttrsMixin[propertyComplexType],
):
    """ A Property element encapsulating :py:class:`~momotor.bundles.binding.momotor.propertyComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        WildcardAttrsMixin.__init__(self)

        self._accept: typing.Optional[str] = None

    @property
    def accept(self) -> typing.Optional[str]:
        return self._accept

    @accept.setter
    def accept(self, accept: typing.Optional[str]):
        assert accept is None or isinstance(accept, str)
        self._accept = accept

    def create(self, *,
               name: str,
               value: typing.Any = None,
               type: str = None,
               accept: str = None,
               attrs: typing.Dict[str, str] = None,
               ) -> "Property":

        self._create_content(name=name, value=value, type=type)

        self.accept = accept
        self.attrs = attrs

        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Property":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Property(target_bundle).create(
            name=self.name,
            value=self.value,
            accept=self.accept,
            attrs=self._attrs,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: propertyComplexType,
                          parent: propertiesComplexType,
                          ref_parent: typing.Optional[propertiesComplexType]) -> "Property":
        self._check_node_type(node, propertyComplexType)
        self._check_node_type(parent, propertiesComplexType)
        self._check_node_type(ref_parent, propertiesComplexType, True)

        super()._create_content_from_node(node, parent, ref_parent)
        super()._create_attrs_from_node(node)

        self.accept = node.accept

        return self

    def _construct_node(self) -> propertyComplexType:
        return (
            self._construct_attrs(
                self._construct_content(
                    propertyComplexType(
                        accept=self.accept,
                    )
                )
            )
        )


# noinspection PyProtectedMember
class PropertiesMixin:
    def __init__(self):
        self._properties: typing.Optional[typing.List[Property]] = None
        self._properties_by_name: typing.Optional[typing.Dict[str, typing.List[Property]]] = None

    @property
    def properties(self) -> typing.Optional[typing.List[Property]]:
        """ `properties` children """
        return None if self._properties is None else [*self._properties]

    @properties.setter
    def properties(self, properties: typing.Iterable[Property]):
        assert properties is None or all(prop.bundle == self.bundle for prop in properties)
        self._properties = None if properties is None else [*properties]
        self._properties_by_name = None

    def _collect_properties(self, parent: complexTypeDefinition) -> typing.List[Property]:
        properties = []
        properties_node = None
        for tag_name, node in get_nested_complex_nodes(parent, 'properties', 'property_'):
            if tag_name == 'properties':
                properties_node = node
            else:
                properties.append(
                    Property(self.bundle)._create_from_node(node, properties_node, None)
                )

        return properties

    # noinspection PyMethodMayBeStatic
    def _construct_properties_nodes(self, properties: typing.Optional[typing.List[Property]]) \
            -> typing.List[propertiesComplexType]:
        if properties:
            return [
                propertiesComplexType(property_=[
                    prop._construct_node()
                    for prop in properties
                ])
            ]

        return []

    def get_properties(self, name: str) -> typing.List[Property]:
        """ Get properties

        :param name: `name` of the properties to get
        :return: A list of all matching properties.
        """
        if self._properties_by_name is None:
            self._properties_by_name = {}
            for prop in self.properties:
                prop_name = prop.name
                if prop_name not in self._properties_by_name:
                    props = self._properties_by_name[prop_name] = []
                else:
                    props = self._properties_by_name[prop_name]

                props.append(prop)

        return self._properties_by_name[name]

    def get_property_value(self, name: str) -> typing.Any:
        """ Get the value for a single property.
        If multiple properties match, the value of the first one found will be returned

        :param name: `name` of the property to get
        :return: The property value
        """
        try:
            return self.get_properties(name)[0].value
        except KeyError:
            return None
