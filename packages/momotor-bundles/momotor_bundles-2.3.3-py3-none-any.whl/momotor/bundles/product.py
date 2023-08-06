import collections.abc
import pathlib
import typing
import zipfile
from pathlib import PurePosixPath

from momotor.bundles.base import Bundle
from momotor.bundles.binding.momotor import productComplexType
from momotor.bundles.const import BundleCategory
from momotor.bundles.elements.base import IdMixin
from momotor.bundles.elements.files import File, FilesMixin
from momotor.bundles.elements.options import Option, OptionsMixin

__all__ = ['ProductBundle']


class ProductBundle(Bundle, IdMixin, OptionsMixin, FilesMixin):
    """ A product bundle. This implements the interface to create and access Momotor product files
    """
    def __init__(self, base: typing.Union[str, pathlib.Path] = None, zip_file: zipfile.ZipFile = None):
        Bundle.__init__(self, base, zip_file)
        IdMixin.__init__(self)
        OptionsMixin.__init__(self)
        FilesMixin.__init__(self)

    # noinspection PyShadowingBuiltins
    def create(self, *,
               id: str = None,
               options: typing.List[Option] = None,
               files: typing.List[File] = None) -> "ProductBundle":
        """ Set all attributes for this ProductBundle

        Usage:

        .. code-block:: python

           product = ProductBundle(...).create(id, options, files)

        :param id: `id` of the bundle (optional)
        :param options: list of options (optional)
        :param files: list of files (optional)
        :return: self
        """
        # TODO meta
        self.id = id
        self.options = options
        self.files = files
        return self

    def recreate(self, target_bundle: "momotor.bundles.Bundle", target_basesrc: PurePosixPath = None) \
            -> typing.NoReturn:
        """ not implemented """
        raise NotImplementedError

    # noinspection PyMethodOverriding
    def _create_from_node(self, node: productComplexType) -> "ProductBundle":
        self._check_node_type(node, productComplexType)

        return self.create(
            id=node.id,
            options=self._collect_options(node, []),
            files=self._collect_files(node, [])
        )

    def _construct_node(self) -> productComplexType:
        return productComplexType(
            id=self.id,
            options=self._construct_options_nodes(self.options),
            files=self._construct_files_nodes(self.files),
        )

    @staticmethod
    def get_default_xml_name():
        """ Get the default XML file name

        :return: 'product.xml'
        """
        return 'product.xml'

    @staticmethod
    def get_root_tag():
        """ Get the XML root tag for this bundle

        :return: 'product'
        """
        return 'product'

    @staticmethod
    def get_category():
        """ Get the category for this bundle

        :return: :py:const:`BundleCategory.PRODUCT`
        """
        return BundleCategory.PRODUCT


# Extend the docstring with the generic documentation of Bundle
ProductBundle.__doc__ += "\n".join(Bundle.__doc__.split("\n")[1:])
