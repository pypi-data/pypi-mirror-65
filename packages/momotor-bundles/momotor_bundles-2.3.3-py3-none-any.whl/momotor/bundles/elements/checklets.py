import collections.abc
import typing
from pathlib import PurePosixPath

from pyxb import BIND
from pyxb.binding.basis import complexTypeDefinition

from momotor.bundles.binding.momotor import checkletComplexType, checkletsComplexType
from momotor.bundles.elements.base import NestedElement
from momotor.bundles.elements.refs import resolve_ref
from momotor.bundles.elements.resources import Resource, ResourcesMixin

__all__ = ['Checklet', 'CheckletMixin']


class Repository(typing.NamedTuple):
    """ A `NamedTuple` for a reference to a repository

    :param src: The src of the repository. Can be a url or a local path
    :type src: str
    :param type: The type of the repository
    :type type: str
    :param revision: The revision of the repository
    :type revision: str
    """
    src: str
    type: str
    revision: str


class Link(typing.NamedTuple):
    """ A `NamedTuple` for a reference to a link

    :param src: The src of the link
    :type src: str
    """
    src: str


class PackageVersion(typing.NamedTuple):
    """ A `NamedTuple` for a reference to a package with version

    :param name: The name of the package
    :type name: str
    :param version: The version qualifier for the package
    :type version: str
    """
    name: str
    version: str


def namedtuple_list_to_nodes(items: typing.Optional[typing.List[typing.NamedTuple]]) \
        -> typing.Optional[typing.List[BIND]]:
    if items:
        # noinspection PyProtectedMember
        return [BIND(**item._asdict()) for item in items if item]


class Checklet(
    NestedElement[checkletComplexType, checkletsComplexType],
    ResourcesMixin,
):
    """ A Checklet element encapsulating :py:class:`~momotor.bundles.binding.momotor.checkletComplexType`

    :param bundle: The element's :py:class:`~momotor.bundles.Bundle`
    :type bundle: :py:class:`~momotor.bundles.Bundle`
    """
    def __init__(self, bundle: "momotor.bundles.Bundle"):
        super().__init__(bundle)
        ResourcesMixin.__init__(self)

        self._name: typing.Optional[str] = None
        self._extras: typing.Optional[typing.List[str]] = None
        self._version: typing.Optional[str] = None
        self._entrypoint: typing.Optional[str] = None
        self._repository: typing.Optional[Repository] = None
        self._link: typing.Optional[Link] = None
        self._indices: typing.Optional[typing.List[Link]] = None
        self._package_versions: typing.Optional[typing.List[PackageVersion]] = None

    @property
    def name(self) -> typing.Optional[str]:
        """ `name` attribute: The Python package name of the checklet """
        return self._name

    @name.setter
    def name(self, name: typing.Optional[str]):
        assert name is None or isinstance(name, str)
        self._name = name

    @property
    def extras(self) -> typing.Optional[typing.List[str]]:
        """ `extras` attribute: The Python package extras (eg. "requests") """
        return None if self._extras is None else [*self._extras]

    @extras.setter
    def extras(self, extras: typing.Optional[typing.Sequence[str]]):
        assert extras is None or isinstance(extras, collections.abc.Sequence)
        self._extras = None if extras is None else [*extras]

    @property
    def version(self) -> typing.Optional[str]:
        """ `version` attribute: A :pep:`440` Python package version specifier (eg. ">=1.0") """
        return self._version

    @version.setter
    def version(self, version: typing.Optional[str]):
        assert version is None or isinstance(version, str)
        self._version = version

    @property
    def entrypoint(self) -> typing.Optional[str]:
        """ `entrypoint` attribute: Override the default package entrypoint (unused, untested) """
        return self._entrypoint

    @entrypoint.setter
    def entrypoint(self, entrypoint: typing.Optional[str]):
        assert entrypoint is None or isinstance(entrypoint, str)
        self._entrypoint = entrypoint

    @property
    def repository(self) -> typing.Optional[Repository]:
        """ `repository` attribute: where to retrieve the package from """
        return self._repository

    @repository.setter
    def repository(self, repository: typing.Optional[Repository]):
        assert repository is None or isinstance(repository, Repository)
        if self._repository:
            # noinspection PyProtectedMember
            self.bundle._unregister_attachment(PurePosixPath(self._repository.src))

        self._repository = repository

        if repository:
            # noinspection PyProtectedMember
            self.bundle._register_attachment(PurePosixPath(repository.src))

    @property
    def link(self) -> typing.Optional[Link]:
        """ `link` attribute: (unused, untested) """
        return self._link

    @link.setter
    def link(self, link: typing.Optional[Link]):
        assert link is None or isinstance(link, Link)
        if self._link:
            # noinspection PyProtectedMember
            self.bundle._unregister_attachment(PurePosixPath(self._link.src))

        self._link = link

        if link:
            # noinspection PyProtectedMember
            self.bundle._register_attachment(PurePosixPath(link.src))

    @property
    def indices(self) -> typing.Optional[typing.List[Link]]:
        """ `indices` attribute: (unused, untested) """
        return None if self._indices is None else [*self._indices]

    @indices.setter
    def indices(self, indices: typing.Optional[typing.Sequence[Link]]):
        assert indices is None or isinstance(indices, collections.abc.Sequence)
        if indices is not None:
            raise ValueError("'Index' type checklets are not supported yet")

    @property
    def package_versions(self) -> typing.Optional[typing.List[PackageVersion]]:
        """ `package_versions` attribute: (unused, untested) """
        return None if self._package_versions is None else [*self._package_versions]

    @package_versions.setter
    def package_versions(self, package_versions: typing.Optional[typing.Sequence[PackageVersion]]):
        assert package_versions is None or isinstance(package_versions, collections.abc.Sequence)
        self._package_versions = None if package_versions is None else [*package_versions]

    # noinspection PyAttributeOutsideInit
    def create(self,
               name: str = None,
               extras: typing.Sequence[str] = None,
               version: str = None,
               entrypoint: str = None,
               repository: Repository = None,
               link: Link = None,
               indices: typing.List[Link] = None,
               package_versions: typing.Sequence[PackageVersion] = None,
               resources: typing.Sequence[Resource] = None,
               ) -> "Checklet":

        self.name = name
        self.extras = extras
        self.version = version
        self.entrypoint = entrypoint
        self.repository = repository
        self.link = link
        self.indices = indices
        self.package_versions = package_versions
        self.resources = resources
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle",
                 target_basesrc: PurePosixPath = None) -> "Checklet":
        assert target_basesrc is None or isinstance(target_basesrc, PurePosixPath)

        return Checklet(target_bundle).create(
            name=self.name,
            extras=self.extras,
            version=self.version,
            entrypoint=self.entrypoint,
            repository=self.repository,
            link=self.link,
            indices=self.indices,
            package_versions=self.package_versions,
            resources=self.resources,
        )

    def _create_from_node(self, node: checkletComplexType, parent: checkletsComplexType = None) -> "Checklet":
        self._check_node_type(node, checkletComplexType)
        self._check_node_type(parent, checkletsComplexType, True)

        name = []
        if parent and parent.basename:
            name.append(parent.basename)
        if node.name:
            name.append(node.name)

        extras = [extra.strip() for extra in node.extras.split(',')] if node.extras else None

        if node.repository:
            assert len(node.repository) == 1
            repository = Repository(node.repository[0].src, node.repository[0].type, node.repository[0].revision)
        else:
            repository = None

        if node.link:
            assert len(node.link) == 1
            # assert not repository
            link = Link(node.link[0].src)
        else:
            link = None

        if node.index:
            assert not repository
            assert not link
            indices = [
                Link(src=index.src) for index in node.index
            ]
        else:
            indices = None

        if node.package_version:
            package_versions = [
                PackageVersion(package_version.name, package_version.version)
                for package_version in node.package_version
            ]
        else:
            package_versions = None

        return self.create(
            name='.'.join(name) if name else None,
            extras=extras,
            version=node.version,
            entrypoint=node.entrypoint,
            repository=repository,
            link=link,
            indices=indices,
            package_versions=package_versions,
            resources=self._collect_resources(node)
        )

    def _construct_node(self) -> checkletComplexType:
        return checkletComplexType(
            name=self.name,
            extras=','.join(self.extras) if self.extras else None,
            version=self.version,
            entrypoint=self.entrypoint,
            repository=namedtuple_list_to_nodes([self.repository]),
            link=namedtuple_list_to_nodes([self.link]),
            index=namedtuple_list_to_nodes(self.indices),
            package_version=namedtuple_list_to_nodes(self.package_versions),
            resources=self._construct_resources_nodes(self.resources),
        )


class CheckletMixin:
    def _collect_checklet(self, node, ref_groups: typing.Iterable[typing.Iterable[complexTypeDefinition]]) \
            -> typing.Optional[Checklet]:

        # TODO use top-level <checklets> node and refs
        if node.checklet:
            if len(node.checklet) > 1:
                raise ValueError("Only one <checklet> node allowed")

            ref_parent, checklet_node = resolve_ref('checklet', node.checklet[0], ref_groups)
            # noinspection PyProtectedMember
            return Checklet(self.bundle)._create_from_node(checklet_node, ref_parent)

        return None
