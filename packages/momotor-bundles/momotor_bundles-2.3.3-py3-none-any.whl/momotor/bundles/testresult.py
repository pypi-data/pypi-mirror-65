import collections.abc
import pathlib
import typing
import zipfile
from collections import OrderedDict
from pathlib import PurePosixPath

from momotor.bundles.base import Bundle
from momotor.bundles.binding.momotor import testResultComplexType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.results import Results

__all__ = ['TestResultBundle']


class TestResultBundle(Bundle):
    """ A test results bundle. This implements the interface to create and access Momotor result files containing
    test results
    """
    __test__ = False  # Prevent pytest from using this as a test case

    def __init__(self, base: typing.Union[str, pathlib.Path] = None, zip_file: zipfile.ZipFile = None):
        Bundle.__init__(self, base, zip_file)

        self._results: typing.OrderedDict[str, Results] = OrderedDict()

    @property
    def results(self) -> typing.List[Results]:
        """ `results` """
        return list(self._results.values())

    @results.setter
    def results(self, results: typing.Optional[typing.Iterable[Results]]):
        assert results is None or (
                isinstance(results, collections.abc.Iterable) and all(result.bundle == self for result in results)
        )
        if results:
            self._results = OrderedDict((results_bundle.id, results_bundle) for results_bundle in results)
        else:
            self._results = OrderedDict()

    def create(self, *, results: typing.Iterable[Results] = None) -> "TestResultBundle":
        """ Set all attributes for this TestResultBundle

        Usage:

        .. code-block:: python

           test_result = TestResultBundle(...).create(results)

        :param results: list of results (optional)
        :return: self
        """
        self.results = results
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        raise NotImplementedError

    # noinspection PyMethodOverriding,PyProtectedMember
    def _create_from_node(self, node: testResultComplexType) -> "TestResultBundle":
        self._check_node_type(node, testResultComplexType)

        return self.create(
            results=(
                Results(self)._create_from_node(results, node) for results in node.results
            ) if node.results else None
        )

    # noinspection PyProtectedMember
    def _construct_node(self) -> testResultComplexType:
        return testResultComplexType(
            results=[
                results._construct_node() for results in self._results.values()
            ] if self.results else None
        )

    @staticmethod
    def get_default_xml_name():
        """ Get the default XML file name

        :return: 'result.xml'
        """
        return 'result.xml'

    @staticmethod
    def get_root_tag():
        """ Get the XML root tag for this bundle

        :return: 'testresult'
        """
        return 'testresult'

    @staticmethod
    def get_category():
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.TEST_RESULTS`
        """
        return BundleCategory.TEST_RESULTS


# Extend the docstring with the generic documentation of Bundle
TestResultBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
