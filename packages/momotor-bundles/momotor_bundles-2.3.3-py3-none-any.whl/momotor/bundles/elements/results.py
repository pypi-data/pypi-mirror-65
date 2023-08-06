import collections.abc
import typing
from pathlib import PurePosixPath

from momotor.bundles.binding.momotor import resultsComplexType, testResultComplexType
from momotor.bundles.elements.base import Element, IdMixin
from momotor.bundles.elements.result import Result
from momotor.bundles.utils.keyedlist import KeyedList

__all__ = ['Results', 'ResultKeyedList']


RT = typing.TypeVar('RT', bound="Results")


ResultsType = typing.Union[KeyedList[Result], typing.Mapping[str, Result], typing.Sequence[Result]]


class ResultKeyedList(KeyedList[Result]):
    """ The results as a :py:class:`~momotor.bundles.utils.keyedlist.KeyedList`
    of :py:class:`~momotor.bundles.elements.result.Result` objects.

    The KeyedList allows access as a list or a mapping. Results are indexed by their `step_id` attribute
    """

    def __init__(self, results: ResultsType = None):
        super().__init__(results, key_attr='step_id')


# noinspection PyProtectedMember
class Results(Element[resultsComplexType], IdMixin):
    """ A Results element encapsulating :py:class:`~momotor.bundles.binding.momotor.resultsComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        IdMixin.__init__(self)
        self._results = ResultKeyedList()

    @property
    def results(self) -> ResultKeyedList:
        # TODO raise exception if results was not initialized yet (this is a breaking change)
        return self._results.copy()

    @results.setter
    def results(self, results: typing.Optional[typing.Sequence[Result]]):
        assert results is None or (
            isinstance(results, collections.abc.Sequence) and all(result.bundle == self.bundle for result in results)
        )

        self._results = ResultKeyedList(results)

    def create(self: RT, *, id: str = None, results: ResultsType = None) -> RT:
        # TODO: meta
        self.id = id
        self.results = results
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: resultsComplexType, testresult: testResultComplexType = None) -> "Results":
        self._check_node_type(node, resultsComplexType)
        self._check_node_type(testresult, testResultComplexType, True)

        return self.create(
            id=node.id,
            results=[
                Result(self.bundle)._create_from_node(result, node) for result in node.result
            ] if node.result else None
        )

    def _construct_node(self) -> resultsComplexType:
        return resultsComplexType(
            id=self.id,
            result=[
                result._construct_node() for result in self._results.values()
            ] if self.results else None
        )
