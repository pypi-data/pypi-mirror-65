import typing
from pathlib import PurePosixPath

from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.binding.momotor import resourceComplexType, resourcesComplexType
from momotor.bundles.elements.content import ContentElement
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['Resource', 'ResourcesMixin']


class Resource(ContentElement[resourceComplexType, resourcesComplexType]):
    """ A Resource element encapsulating :py:class:`~momotor.bundles.binding.momotor.resourceComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)

    def create(self, *, name: str, value: str = None) -> "Resource":
        self._create_content(name=name, value=value)
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> "Resource":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Resource(target_bundle).create(
            name=self.name,
            value=self.value
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: resourceComplexType,
                          direct_parent: resourcesComplexType,
                          ref_parent: typing.Optional[resourcesComplexType]) -> "Resource":
        self._check_node_type(node, resourceComplexType)
        self._check_node_type(direct_parent, resourcesComplexType)
        self._check_node_type(ref_parent, resourcesComplexType, True)

        self._create_content_from_node(node, direct_parent, ref_parent)

        return self

    def _construct_node(self) -> resourceComplexType:
        return (
            self._construct_content(
                resourceComplexType()
            )
        )


# noinspection PyProtectedMember
class ResourcesMixin:
    def __init__(self):
        self._resources: typing.Optional[typing.List[Resource]] = None
        self._resources_by_name: typing.Optional[typing.Dict[str, typing.List[Resource]]] = None

    @property
    def resources(self) -> typing.Optional[typing.List[Resource]]:
        """ `resources` attribute """
        return None if self._resources is None else [*self._resources]

    @resources.setter
    def resources(self, resources: typing.Optional[typing.Sequence[Resource]]):
        assert resources is None or all(resource.bundle == self.bundle for resource in resources)
        self._resources = None if resources is None else [*resources]
        self._resources_updated()

    def _resources_updated(self):
        self._resources_by_name = None

    def _collect_resources(self, parent: complexTypeDefinition) -> typing.List[Resource]:
        resources = []
        resources_node = None
        for tag_name, node in get_nested_complex_nodes(parent, 'resources', 'resource'):
            if tag_name == 'resources':
                resources_node = node
            else:
                resources.append(
                    Resource(self.bundle)._create_from_node(node, resources_node, None)
                )

        return resources

    # noinspection PyMethodMayBeStatic
    def _construct_resources_nodes(self, resources: typing.Optional[typing.List[Resource]]) \
            -> typing.List[resourcesComplexType]:
        if resources:
            return [
                resourcesComplexType(resource=[
                    resource._construct_node()
                    for resource in resources
                ])
            ]

        return []

    def _get_resources(self) -> typing.Dict[str, typing.List[Resource]]:
        if self._resources_by_name is None:
            self._resources_by_name = {}
            for resource in self.resources:
                name = resource.name
                if name not in self._resources_by_name:
                    resources = self._resources_by_name[name] = []
                else:
                    resources = self._resources_by_name[name]

                resources.append(resource)

        return self._resources_by_name

    def get_resources(self) -> typing.Dict[str, typing.List[Resource]]:
        """ Get the resources as a dictionary name -> Resource """
        return self._get_resources()
