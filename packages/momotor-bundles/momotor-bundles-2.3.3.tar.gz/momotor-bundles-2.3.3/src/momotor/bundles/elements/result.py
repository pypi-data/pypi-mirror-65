import typing
import warnings
from pathlib import PurePosixPath

from momotor.bundles.binding.momotor import resultComplexType, resultsComplexType
from momotor.bundles.elements.base import NestedElement
from momotor.bundles.elements.checklets import CheckletMixin, Checklet
from momotor.bundles.elements.files import FilesMixin, File
from momotor.bundles.elements.options import Option, OptionsMixin
from momotor.bundles.elements.properties import PropertiesMixin, Property

__all__ = ['Result', 'create_error_result']


class Result(
    NestedElement[resultComplexType, resultsComplexType],
    CheckletMixin, PropertiesMixin, OptionsMixin, FilesMixin
):
    """ A Result element encapsulating :py:class:`~momotor.bundles.binding.momotor.resultComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        CheckletMixin.__init__(self)
        PropertiesMixin.__init__(self)
        OptionsMixin.__init__(self)
        FilesMixin.__init__(self)

        self._attachments_group_id: typing.Optional[str] = None
        self._step_id: typing.Optional[str] = None
        self._outcome: typing.Optional[str] = None
        self._checklet: typing.Optional[Checklet] = None
        self._parent_id: typing.Optional[str] = None

    @property
    def step_id(self) -> str:
        """ `step_id` attribute """
        if self._step_id is None:
            raise ValueError("Result not initialized: step_id not yet set")

        return self._step_id

    @step_id.setter
    def step_id(self, step_id: str):
        assert isinstance(step_id, str)
        self._step_id = step_id
        self._update_attachments_group_id()

    @property
    def outcome(self):
        """ `outcome` attribute. Valid values are ``pass``, ``fail`` and ``error`` """
        if self._outcome is None:
            raise ValueError("Result not initialized: outcome not yet set")

        return self._outcome

    @outcome.setter
    def outcome(self, outcome: str):
        assert isinstance(outcome, str)
        if outcome not in {'pass', 'fail', 'error'}:
            warnings.warn(f"Invalid outcome attribute value '{outcome}' ignored (will use 'error')")
            outcome = 'error'

        self._outcome = outcome

    @property
    def checklet(self) -> typing.Optional[Checklet]:
        """ `checklet` """
        return self._checklet

    @checklet.setter
    def checklet(self, checklet: typing.Optional[Checklet]):
        assert checklet is None or (isinstance(checklet, Checklet) and checklet.bundle == self.bundle)
        self._checklet = checklet

    def set_parent_id(self, parent_id: typing.Optional[str]):
        """ Set the id of the result parent """
        assert parent_id is None or isinstance(parent_id, str)
        assert not self._has_files, "parent id must be set before files are added"
        self._parent_id = parent_id
        self._update_attachments_group_id()

    def _update_attachments_group_id(self):
        if self._step_id:
            if self._parent_id:
                self._attachments_group_id = f'{self._step_id}@{self._parent_id}'
            else:
                self._attachments_group_id = self._step_id
        elif self._parent_id:
            self._attachments_group_id = f'@{self._parent_id}'

    def create(self, *,
               step_id: str,
               outcome: str,
               checklet: Checklet = None,
               properties: typing.List[Property] = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None,
               parent_id: str = None,
               ) -> "Result":

        self.set_parent_id(parent_id)
        self.step_id = step_id
        self.outcome = outcome
        self.checklet = checklet
        self.properties = properties
        self.options = options
        self.files = files
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "Result":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Result(target_bundle).create(
            step_id=self.step_id,
            outcome=self.outcome,
            checklet=self.checklet.recreate(target_bundle) if self.checklet is not None else None,
            properties=self.recreate_list(self.properties, target_bundle, target_basesrc),
            options=self.recreate_list(self.options, target_bundle, target_basesrc),
            files=self.recreate_list(self.files, target_bundle, target_basesrc),
            parent_id=self._parent_id,
        )

    def _create_from_node(self, node: resultComplexType, results: resultsComplexType = None) -> "Result":
        self._check_node_type(node, resultComplexType)
        self._check_node_type(results, resultsComplexType, True)

        return self.create(
            step_id=node.step,
            outcome=node.outcome,
            checklet=self._collect_checklet(node, [results.checklets] if results else None),
            properties=self._collect_properties(node),
            options=self._collect_options(node, []),
            files=self._collect_files(node, []),
            parent_id=results.id if results else None,
        )

    def _construct_node(self) -> resultComplexType:
        return resultComplexType(
            step=self.step_id,
            outcome=self.outcome,
            # TODO checklet
            properties=self._construct_properties_nodes(self.properties),
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
        )

    @property
    def passed(self) -> bool:
        """ Returns True if `outcome` is ``pass`` """
        return self.outcome == 'pass'

    @property
    def failed(self) -> bool:
        """ Returns True if `outcome` is ``fail`` """
        return self.outcome == 'fail'

    @property
    def erred(self) -> bool:
        """ Returns True if `outcome` is ``error`` """
        return self.outcome == 'error'


def create_error_result(bundle, step_id, status, report=None):
    """ Create an error result """
    return Result(bundle).create(
        step_id=step_id,
        outcome='error',
        properties=[
            Property(bundle).create(name='status', type='string', value=status),
            Property(bundle).create(name='report', type='string', value=report or status),
        ]
    )
