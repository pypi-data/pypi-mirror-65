import collections.abc
import typing
from pathlib import PurePosixPath, Path

from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.binding.momotor import fileComplexType, filesComplexType
from momotor.bundles.elements.content import ContentSrcElement
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.wildcard import WildcardAttrsMixin
from momotor.bundles.utils.nodes import get_nested_complex_nodes

__all__ = ['File', 'FilesMixin']


# def merge(ls: typing.Iterable = None, extra=None) -> typing.List:
#     """ Filter all None values from `ls`, append `extra` """
#     ls = [item for item in ls if item is not None] if ls else []
#     if extra is not None:
#         ls.append(extra)
#     return ls


class File(
    ContentSrcElement[fileComplexType, filesComplexType],
    WildcardAttrsMixin[fileComplexType]
):
    """ A File element encapsulating :py:class:`~momotor.bundles.binding.momotor.fileComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        WildcardAttrsMixin.__init__(self)

        self._class: typing.Optional[str] = None

    @property
    def class_(self) -> typing.Optional[str]:
        """ `class` attribute """
        return self._class

    @class_.setter
    def class_(self, class_: typing.Optional[str]):
        assert class_ is None or isinstance(class_, str)
        self._class = class_

    def create(self, *,
               class_: str = None,
               name: typing.Union[str, PurePosixPath] = None,
               src: PurePosixPath = None,
               content: typing.Union[bytes, str] = None,
               type: str = None,
               attrs: typing.Mapping[str, str] = None,
               ) -> "File":

        self._create_content(name=name, value=content, src=src, type=type)

        self.attrs = attrs
        self.class_ = class_

        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) -> "File":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return File(target_bundle).create(
            class_=self.class_,
            name=self.name,
            src=self._recreate_src(target_bundle, target_basesrc),
            content=self.value,
            attrs=self._attrs,
        )

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: fileComplexType,
                          direct_parent: filesComplexType,
                          ref_parent: typing.Optional[filesComplexType]) -> "File":
        self._check_node_type(node, fileComplexType)
        self._check_node_type(direct_parent, filesComplexType)
        self._check_node_type(ref_parent, filesComplexType, True)

        self._create_content_from_node(node, direct_parent, ref_parent)
        self._create_attrs_from_node(node)

        class_parts = self._get_attr_base_parts('class_', node, direct_parent, ref_parent, base_attr='baseclass',
                                                allow_base_only=True)
        self.class_ = '.'.join(class_parts) if class_parts else None

        return self

    def _construct_node(self) -> fileComplexType:
        return (
            self._construct_attrs(
                self._construct_content(
                    fileComplexType(
                        class_=self.class_,
                    )
                )
            )
        )

    def _join_name(self, parts: typing.Iterable):
        return PurePosixPath(*parts)


# noinspection PyProtectedMember
class FilesMixin:
    """ Mixin for `Element` to add file support.
    """
    def __init__(self):
        self._has_files = False

    def _collect_files(self, parent: complexTypeDefinition,
                       ref_parents: typing.Iterable[typing.Iterable[filesComplexType]]) \
            -> typing.List[File]:

        files = []
        files_node = None
        for tag_name, node in get_nested_complex_nodes(parent, 'files', 'file'):
            if tag_name == 'files':
                files_node = node
            else:
                if ref_parents:
                    ref_parent, node = resolve_ref('file', node, ref_parents)
                else:
                    ref_parent = None

                files.append(
                    File(self.bundle)._create_from_node(node, files_node, ref_parent)
                )

        return files

    # noinspection PyMethodMayBeStatic
    def _construct_files_nodes(self, files: typing.Optional[typing.List[File]]) -> typing.List[filesComplexType]:
        # TODO group by class
        if files:
            return [
                filesComplexType(file=[
                    file._construct_node()
                    for file in files
                ])
            ]

        return []

    def _get_attachment_group_id(self):
        return getattr(self, '_attachments_group_id', getattr(self, 'id', '')) or ''

    @property
    def files(self) -> typing.Optional[typing.List[File]]:
        """ The files
        """
        return self.bundle._get_files(self._get_attachment_group_id())

    @files.setter
    def files(self, files: typing.Optional[typing.List[File]]):
        if files is not None:
            assert isinstance(files, collections.abc.Sequence) and all(file.bundle == self.bundle for file in files)
            self._has_files = True
            self.bundle._set_files(self._get_attachment_group_id(), files)

    def copy_files(self, dest_dir: Path) -> None:
        """ Copy the files to `dest_dir` """
        self.bundle._copy_files(dest_dir, self._get_attachment_group_id())
