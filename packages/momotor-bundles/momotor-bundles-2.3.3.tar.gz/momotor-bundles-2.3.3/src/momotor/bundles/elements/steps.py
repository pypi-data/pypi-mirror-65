import collections.abc
import copy
import typing
from enum import IntEnum
from pathlib import PurePosixPath

from momotor.bundles.binding.momotor import dependsComplexType, stepComplexType, dependenciesComplexType, \
    stepsComplexType, recipeComplexType
from momotor.bundles.elements.base import Element, NestedElement, IdMixin
from momotor.bundles.elements.checklets import Checklet, CheckletMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.resources import ResourcesMixin, Resource
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['Priority', 'Depends', 'Step']


class Priority(IntEnum):
    """ An enum for the step priority """
    MUST_PASS = 0
    HIGH = 1
    NORMAL = 2
    DEFAULT = 2
    LOW = 3


PRIORITY_LEVELS = 4
PRIORITIES_MAP = {
    'must-pass': Priority.MUST_PASS,
    'high': Priority.HIGH,
    'default': Priority.DEFAULT,
    'normal': Priority.NORMAL,
    'low': Priority.LOW,
}
PRIORITY_NAME = dict((prio.value, name) for name, prio in PRIORITIES_MAP.items())


class Depends(Element[dependsComplexType], OptionsMixin):
    """ A Depends element encapsulating :py:class:`~momotor.bundles.binding.momotor.dependsComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        OptionsMixin.__init__(self)

        self._step: typing.Optional[str] = None

    @property
    def step(self) -> str:
        """ `step` attribute """
        assert self._step is not None
        return self._step

    @step.setter
    def step(self, step: str):
        assert isinstance(step, str)
        self._step = step

    def create(self, *,
               step: str,
               options: typing.List[Option] = None
               ) -> "Depends":

        self.step = step
        self.options = options
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Depends":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Depends(target_bundle).create(
            step=self.step,
            options=self.options,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: dependsComplexType) -> "Depends":
        self._check_node_type(node, dependsComplexType)

        return self.create(
            step=node.step,
            options=self._collect_options(node, []),
        )

    def _construct_node(self) -> dependsComplexType:
        return dependsComplexType(
            step=self.step,
            options=self._construct_options_nodes(self.options),
        )


# noinspection PyProtectedMember
class Step(
    NestedElement[stepComplexType, stepsComplexType],
    IdMixin, CheckletMixin, OptionsMixin, FilesMixin, ResourcesMixin,
):
    """ A Step element encapsulating :py:class:`~momotor.bundles.binding.momotor.stepComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        IdMixin.__init__(self)
        OptionsMixin.__init__(self)
        FilesMixin.__init__(self)
        ResourcesMixin.__init__(self)

        self._priority: typing.Optional[str] = None
        self._depends: typing.Optional[typing.List[Depends]] = None
        self._checklet: typing.Optional[Checklet] = None
        self._merged_resources = None

    @property
    def priority(self) -> str:
        """ `priority` attribute """
        assert self._priority is not None
        return self._priority

    @priority.setter
    def priority(self, priority: str):
        assert priority in PRIORITIES_MAP
        self._priority = priority

    @property
    def depends(self) -> typing.Optional[typing.List[Depends]]:
        """ `depends` """
        return self._depends

    @depends.setter
    def depends(self, depends: typing.List[Depends]):
        assert depends is None or (
            isinstance(depends, collections.abc.Sequence) and all(depend.bundle == self.bundle for depend in depends)
        )
        self._depends = [*depends] if depends is not None else None

    @property
    def checklet(self) -> typing.Optional[Checklet]:
        """ `checklet` """
        return self._checklet

    @checklet.setter
    def checklet(self, checklet: Checklet):
        assert checklet is None or (isinstance(checklet, Checklet) and checklet.bundle == self.bundle)
        self._checklet = checklet
        self._merged_resources = None

    def _resources_updated(self):
        super()._resources_updated()
        self._merged_resources = None

    # noinspection PyAttributeOutsideInit
    def create(self, *,
               id: str,
               priority: str = 'default',
               depends: typing.List[Depends] = None,
               checklet: Checklet = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None,
               resources: typing.List[Resource] = None,
               ) -> "Step":

        self.id = id
        self.priority = priority
        self.depends = depends
        self.checklet = checklet
        self.options = options
        self.files = files
        self.resources = resources
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: stepComplexType, steps: stepsComplexType, recipe: recipeComplexType) -> "Step":
        # recipe > steps > step
        #
        # step has <files> children
        #  - file.ref can refer to file in recipe.files
        #
        # step has single <checklet> child
        #  - checklet.ref can refer to checklet in steps.checklets or recipe.checklets

        self._check_node_type(node, stepComplexType)
        self._check_node_type(steps, stepsComplexType)
        self._check_node_type(recipe, recipeComplexType)

        return self.create(
            id=node.id,
            priority=node.priority,
            depends=self._collect_depends(node),
            checklet=self._collect_checklet(node, [steps.checklets, recipe.checklets]),
            options=self._collect_options(node, [steps.options, recipe.options]),
            files=self._collect_files(node, [recipe.files]),
            resources=self._collect_resources(node)
        )

    def _collect_depends(self, node: stepComplexType) -> typing.List[Depends]:
        depends = []
        for tag_name, child in get_nested_complex_nodes(node, 'dependencies', 'depends'):
            if tag_name == 'depends':
                depends.append(Depends(self.bundle)._create_from_node(node=child))

        return depends

    def _construct_node(self) -> stepComplexType:
        return stepComplexType(
            id=self.id,
            priority=self.priority,
            dependencies=[dependenciesComplexType(
                depends=[dep._construct_node() for dep in self.depends]
            )],
            checklet=[self.checklet._construct_node()] if self.checklet else [],
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
            resources=self._construct_resources_nodes(self.resources),
        )

    @property
    def priority_value(self) -> Priority:
        """ `priority` attribute as :py:class:`Priority` instance """
        return PRIORITIES_MAP[self.priority]

    def get_dependencies_ids(self) -> typing.List[str]:
        """ ids of the dependencies """
        return [
            depends.step for depends in self.depends
        ]

    def get_resources(self) -> typing.Dict[str, typing.List[Resource]]:
        """ get all resources needed by this step """
        if self._merged_resources is None:
            merged_resources = copy.deepcopy(self._get_resources())
            if self.checklet:
                for name, resources in self.checklet.get_resources().items():
                    if name in merged_resources:
                        merged_resources[name].extend(resources)
                    else:
                        merged_resources[name] = resources[:]

            self._merged_resources = merged_resources

        return self._merged_resources
