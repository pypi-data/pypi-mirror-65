import collections.abc
import pathlib
import typing
import zipfile
from collections import OrderedDict
from pathlib import PurePosixPath

from momotor.bundles.base import Bundle
from momotor.bundles.binding.momotor import recipeComplexType, stepsComplexType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.base import IdMixin
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.steps import Step
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['RecipeBundle']


class RecipeBundle(Bundle, IdMixin, OptionsMixin):
    """ A recipe bundle. This implements the interface to create and access Momotor recipe files
    """
    # Recipe options are only used from refs, so don't have to be processed here
    def __init__(self, base: typing.Union[str, pathlib.Path] = None, zip_file: zipfile.ZipFile = None):
        Bundle.__init__(self, base, zip_file)
        IdMixin.__init__(self)
        OptionsMixin.__init__(self)
        self._steps: typing.Optional[typing.Dict[str, Step]] = None
        self._tests: typing.Optional[typing.Dict[str, typing.Any]] = None

    @property
    def steps(self) -> typing.Optional[typing.Dict[str, Step]]:
        """ The recipe's `steps` """
        return None if self._steps is None else {**self._steps}

    @steps.setter
    def steps(self, steps: typing.Optional[typing.Mapping[str, Step]]):
        assert isinstance(steps, collections.abc.Mapping) and all(step.bundle == self for step in steps.values())
        self._steps = None if steps is None else {**steps}

    @property
    def tests(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """ The recipe's `tests` (not implemented yet) """
        return None if self._tests is None else {**self._tests}

    @tests.setter
    def tests(self, tests: typing.Optional[typing.Mapping[str, typing.Any]]):
        assert isinstance(tests, collections.abc.Mapping) and all(test.bundle == self for test in tests.values())
        if tests:
            raise NotImplementedError

    # noinspection PyAttributeOutsideInit
    def create(self, *,
               id: str = None,
               options: typing.List[Option] = None,
               steps: typing.Dict[str, Step],
               tests: typing.Dict[str, typing.Any],
               ) -> "RecipeBundle":
        """ Set all attributes for this RecipeBundle

        Usage:

        .. code-block:: python

           recipe = RecipeBundle(...).create(id, options, steps, tests)

        :param id: `id` of the bundle (optional)
        :param options: list of options (optional)
        :param steps: dictionary of steps with step_id as key
        :param tests: dictionary of tests with test_id as key
        :return: self
        """
        self.id = id
        self.options = options
        self.steps = steps
        self.tests = tests
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding,PyProtectedMember
    def _create_from_node(self, node: recipeComplexType) -> "RecipeBundle":
        self._check_node_type(node, recipeComplexType)

        steps = OrderedDict()
        steps_node = None
        for tag_name, child_node in get_nested_complex_nodes(node, 'steps', 'step'):
            if tag_name == 'steps':
                steps_node = child_node
            else:
                steps[child_node.id] = Step(self)._create_from_node(child_node, steps_node, node)

        return self.create(
            id=node.id,
            options=self._collect_options(node, []),
            steps=steps,
            tests={},  # TODO
        )

    # noinspection PyProtectedMember
    def _construct_node(self) -> recipeComplexType:
        return recipeComplexType(
            id=self.id,
            options=self._construct_options_nodes(self.options),
            steps=[stepsComplexType(step=[
                step._construct_node() for step in self._steps.values()
            ])],
            # tests=testsComplexType(test=[
            #     test._construct_node() for test in self._tests.values()
            # ])  TODO
        )

    @staticmethod
    def get_default_xml_name():
        """ Get the default XML file name

        :return: 'recipe.xml'
        """
        return 'recipe.xml'

    @staticmethod
    def get_root_tag():
        """ Get the XML root tag for this bundle

        :return: 'recipe'
        """
        return 'recipe'

    @staticmethod
    def get_category():
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.RECIPE`
        """
        return BundleCategory.RECIPE


# Extend the docstring with the generic documentation of Bundle
RecipeBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
