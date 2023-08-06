# src\momotor\bundles\binding\momotor.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:6bec1dac88ac4a2ed49ee0a6a98ef4c3832c56b9
# Generated 2019-08-22 09:43:13.639087 by PyXB version 1.2.6 using Python 3.7.4.final.0
# Namespace http://momotor.org/1.0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:7edcd490-c4b0-11e9-ba43-34e12dcc61fd')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.binding.xml_

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://momotor.org/1.0', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 148, 12)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.eq = STD_ANON._CF_enumeration.addEnumeration(unicode_value='eq', tag='eq')
STD_ANON.ne = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ne', tag='ne')
STD_ANON.lt = STD_ANON._CF_enumeration.addEnumeration(unicode_value='lt', tag='lt')
STD_ANON.le = STD_ANON._CF_enumeration.addEnumeration(unicode_value='le', tag='le')
STD_ANON.gt = STD_ANON._CF_enumeration.addEnumeration(unicode_value='gt', tag='gt')
STD_ANON.ge = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ge', tag='ge')
STD_ANON.one_of = STD_ANON._CF_enumeration.addEnumeration(unicode_value='one-of', tag='one_of')
STD_ANON.in_range = STD_ANON._CF_enumeration.addEnumeration(unicode_value='in-range', tag='in_range')
STD_ANON.any = STD_ANON._CF_enumeration.addEnumeration(unicode_value='any', tag='any')
STD_ANON.none = STD_ANON._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: {http://momotor.org/1.0}outcomeSimpleType
class outcomeSimpleType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'outcomeSimpleType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 167, 4)
    _Documentation = None
outcomeSimpleType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=outcomeSimpleType, enum_prefix=None)
outcomeSimpleType.pass_ = outcomeSimpleType._CF_enumeration.addEnumeration(unicode_value='pass', tag='pass_')
outcomeSimpleType.fail = outcomeSimpleType._CF_enumeration.addEnumeration(unicode_value='fail', tag='fail')
outcomeSimpleType.error = outcomeSimpleType._CF_enumeration.addEnumeration(unicode_value='error', tag='error')
outcomeSimpleType._InitializeFacetMap(outcomeSimpleType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'outcomeSimpleType', outcomeSimpleType)
_module_typeBindings.outcomeSimpleType = outcomeSimpleType

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 224, 12)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.must_pass = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='must-pass', tag='must_pass')
STD_ANON_.high = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='high', tag='high')
STD_ANON_.normal = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='normal', tag='normal')
STD_ANON_.low = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='low', tag='low')
STD_ANON_.default = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='default', tag='default')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Complex type {http://momotor.org/1.0}linkComplexType with content type EMPTY
class linkComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}linkComplexType with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'linkComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 21, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__httpmomotor_org1_0_linkComplexType_src', pyxb.binding.datatypes.anyURI, required=True)
    __src._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 22, 8)
    __src._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 22, 8)
    
    src = property(__src.value, __src.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __src.name() : __src
    })
_module_typeBindings.linkComplexType = linkComplexType
Namespace.addCategoryObject('typeBinding', 'linkComplexType', linkComplexType)


# Complex type {http://momotor.org/1.0}metaComplexType with content type ELEMENT_ONLY
class metaComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}metaComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'metaComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 25, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0name', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 27, 12), )

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://momotor.org/1.0}version uses Python identifier version
    __version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'version'), 'version', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0version', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 28, 12), )

    
    version = property(__version.value, __version.set, None, None)

    
    # Element {http://momotor.org/1.0}author uses Python identifier author
    __author = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'author'), 'author', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0author', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 29, 12), )

    
    author = property(__author.value, __author.set, None, None)

    
    # Element {http://momotor.org/1.0}description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'description'), 'description', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0description', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 30, 12), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://momotor.org/1.0}source uses Python identifier source
    __source = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'source'), 'source', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0source', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 41, 12), )

    
    source = property(__source.value, __source.set, None, None)

    
    # Element {http://momotor.org/1.0}generator uses Python identifier generator
    __generator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'generator'), 'generator', '__httpmomotor_org1_0_metaComplexType_httpmomotor_org1_0generator', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 42, 12), )

    
    generator = property(__generator.value, __generator.set, None, None)

    _ElementMap.update({
        __name.name() : __name,
        __version.name() : __version,
        __author.name() : __author,
        __description.name() : __description,
        __source.name() : __source,
        __generator.name() : __generator
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.metaComplexType = metaComplexType
Namespace.addCategoryObject('typeBinding', 'metaComplexType', metaComplexType)


# Complex type [anonymous] with content type MIXED
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 31, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.w3.org/XML/1998/namespace}lang uses Python identifier lang
    __lang = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.XML, 'lang'), 'lang', '__httpmomotor_org1_0_CTD_ANON_httpwww_w3_orgXML1998namespacelang', pyxb.binding.xml_.STD_ANON_lang)
    __lang._DeclarationLocation = None
    __lang._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 35, 20)
    
    lang = property(__lang.value, __lang.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpmomotor_org1_0_CTD_ANON_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    __type._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'encoding'), 'encoding', '__httpmomotor_org1_0_CTD_ANON_encoding', pyxb.binding.datatypes.string)
    __encoding._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    __encoding._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    
    encoding = property(__encoding.value, __encoding.set, None, None)

    
    # Attribute base uses Python identifier base
    __base = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'base'), 'base', '__httpmomotor_org1_0_CTD_ANON_base', pyxb.binding.datatypes.anyURI)
    __base._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 36, 20)
    __base._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 36, 20)
    
    base = property(__base.value, __base.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://momotor.org/1.0'))
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __lang.name() : __lang,
        __type.name() : __type,
        __encoding.name() : __encoding,
        __base.name() : __base
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type {http://momotor.org/1.0}optionsComplexType with content type ELEMENT_ONLY
class optionsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}optionsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'optionsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 46, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}option uses Python identifier option
    __option = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'option'), 'option', '__httpmomotor_org1_0_optionsComplexType_httpmomotor_org1_0option', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 48, 12), )

    
    option = property(__option.value, __option.set, None, None)

    
    # Attribute domain uses Python identifier domain
    __domain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpmomotor_org1_0_optionsComplexType_domain', pyxb.binding.datatypes.string)
    __domain._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 50, 8)
    __domain._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 50, 8)
    
    domain = property(__domain.value, __domain.set, None, None)

    _ElementMap.update({
        __option.name() : __option
    })
    _AttributeMap.update({
        __domain.name() : __domain
    })
_module_typeBindings.optionsComplexType = optionsComplexType
Namespace.addCategoryObject('typeBinding', 'optionsComplexType', optionsComplexType)


# Complex type {http://momotor.org/1.0}optionComplexType with content type MIXED
class optionComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}optionComplexType with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'optionComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 53, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpmomotor_org1_0_optionComplexType_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    __type._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'encoding'), 'encoding', '__httpmomotor_org1_0_optionComplexType_encoding', pyxb.binding.datatypes.string)
    __encoding._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    __encoding._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    
    encoding = property(__encoding.value, __encoding.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_optionComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_optionComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_optionComplexType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 58, 8)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 58, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpmomotor_org1_0_optionComplexType_value', pyxb.binding.datatypes.string)
    __value._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 59, 8)
    __value._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 59, 8)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute domain uses Python identifier domain
    __domain = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'domain'), 'domain', '__httpmomotor_org1_0_optionComplexType_domain', pyxb.binding.datatypes.string)
    __domain._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 60, 8)
    __domain._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 60, 8)
    
    domain = property(__domain.value, __domain.set, None, None)

    
    # Attribute external uses Python identifier external
    __external = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'external'), 'external', '__httpmomotor_org1_0_optionComplexType_external', pyxb.binding.datatypes.boolean)
    __external._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 61, 8)
    __external._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 61, 8)
    
    external = property(__external.value, __external.set, None, None)

    
    # Attribute description uses Python identifier description
    __description = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpmomotor_org1_0_optionComplexType_description', pyxb.binding.datatypes.string)
    __description._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 62, 8)
    __description._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 62, 8)
    
    description = property(__description.value, __description.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __encoding.name() : __encoding,
        __id.name() : __id,
        __ref.name() : __ref,
        __name.name() : __name,
        __value.name() : __value,
        __domain.name() : __domain,
        __external.name() : __external,
        __description.name() : __description
    })
_module_typeBindings.optionComplexType = optionComplexType
Namespace.addCategoryObject('typeBinding', 'optionComplexType', optionComplexType)


# Complex type {http://momotor.org/1.0}filesComplexType with content type ELEMENT_ONLY
class filesComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}filesComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'filesComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 67, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'file'), 'file', '__httpmomotor_org1_0_filesComplexType_httpmomotor_org1_0file', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 69, 12), )

    
    file = property(__file.value, __file.set, None, None)

    
    # Attribute baseclass uses Python identifier baseclass
    __baseclass = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'baseclass'), 'baseclass', '__httpmomotor_org1_0_filesComplexType_baseclass', pyxb.binding.datatypes.string)
    __baseclass._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 71, 8)
    __baseclass._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 71, 8)
    
    baseclass = property(__baseclass.value, __baseclass.set, None, None)

    
    # Attribute basename uses Python identifier basename
    __basename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'basename'), 'basename', '__httpmomotor_org1_0_filesComplexType_basename', pyxb.binding.datatypes.string)
    __basename._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 72, 8)
    __basename._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 72, 8)
    
    basename = property(__basename.value, __basename.set, None, None)

    
    # Attribute basesrc uses Python identifier basesrc
    __basesrc = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'basesrc'), 'basesrc', '__httpmomotor_org1_0_filesComplexType_basesrc', pyxb.binding.datatypes.string)
    __basesrc._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 73, 8)
    __basesrc._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 73, 8)
    
    basesrc = property(__basesrc.value, __basesrc.set, None, None)

    _ElementMap.update({
        __file.name() : __file
    })
    _AttributeMap.update({
        __baseclass.name() : __baseclass,
        __basename.name() : __basename,
        __basesrc.name() : __basesrc
    })
_module_typeBindings.filesComplexType = filesComplexType
Namespace.addCategoryObject('typeBinding', 'filesComplexType', filesComplexType)


# Complex type {http://momotor.org/1.0}fileComplexType with content type MIXED
class fileComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}fileComplexType with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 76, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpmomotor_org1_0_fileComplexType_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    __type._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'encoding'), 'encoding', '__httpmomotor_org1_0_fileComplexType_encoding', pyxb.binding.datatypes.string)
    __encoding._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    __encoding._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    
    encoding = property(__encoding.value, __encoding.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_fileComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_fileComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_fileComplexType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 81, 8)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 81, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute class uses Python identifier class_
    __class = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'class'), 'class_', '__httpmomotor_org1_0_fileComplexType_class', pyxb.binding.datatypes.string)
    __class._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 82, 8)
    __class._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 82, 8)
    
    class_ = property(__class.value, __class.set, None, None)

    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__httpmomotor_org1_0_fileComplexType_src', pyxb.binding.datatypes.string)
    __src._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 83, 8)
    __src._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 83, 8)
    
    src = property(__src.value, __src.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __encoding.name() : __encoding,
        __id.name() : __id,
        __ref.name() : __ref,
        __name.name() : __name,
        __class.name() : __class,
        __src.name() : __src
    })
_module_typeBindings.fileComplexType = fileComplexType
Namespace.addCategoryObject('typeBinding', 'fileComplexType', fileComplexType)


# Complex type {http://momotor.org/1.0}resourceComplexType with content type MIXED
class resourceComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}resourceComplexType with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resourceComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 88, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_resourceComplexType_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 92, 8)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 92, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpmomotor_org1_0_resourceComplexType_value', pyxb.binding.datatypes.string)
    __value._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 93, 8)
    __value._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 93, 8)
    
    value_ = property(__value.value, __value.set, None, None)

    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __value.name() : __value
    })
_module_typeBindings.resourceComplexType = resourceComplexType
Namespace.addCategoryObject('typeBinding', 'resourceComplexType', resourceComplexType)


# Complex type {http://momotor.org/1.0}resourcesComplexType with content type ELEMENT_ONLY
class resourcesComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}resourcesComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resourcesComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 96, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}resource uses Python identifier resource
    __resource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'resource'), 'resource', '__httpmomotor_org1_0_resourcesComplexType_httpmomotor_org1_0resource', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 98, 12), )

    
    resource = property(__resource.value, __resource.set, None, None)

    _ElementMap.update({
        __resource.name() : __resource
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.resourcesComplexType = resourcesComplexType
Namespace.addCategoryObject('typeBinding', 'resourcesComplexType', resourcesComplexType)


# Complex type {http://momotor.org/1.0}checkletsComplexType with content type ELEMENT_ONLY
class checkletsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}checkletsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'checkletsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 102, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}checklet uses Python identifier checklet
    __checklet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklet'), 'checklet', '__httpmomotor_org1_0_checkletsComplexType_httpmomotor_org1_0checklet', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 104, 12), )

    
    checklet = property(__checklet.value, __checklet.set, None, None)

    
    # Attribute basename uses Python identifier basename
    __basename = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'basename'), 'basename', '__httpmomotor_org1_0_checkletsComplexType_basename', pyxb.binding.datatypes.string)
    __basename._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 106, 8)
    __basename._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 106, 8)
    
    basename = property(__basename.value, __basename.set, None, None)

    _ElementMap.update({
        __checklet.name() : __checklet
    })
    _AttributeMap.update({
        __basename.name() : __basename
    })
_module_typeBindings.checkletsComplexType = checkletsComplexType
Namespace.addCategoryObject('typeBinding', 'checkletsComplexType', checkletsComplexType)


# Complex type {http://momotor.org/1.0}checkletComplexType with content type ELEMENT_ONLY
class checkletComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}checkletComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'checkletComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 109, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}repository uses Python identifier repository
    __repository = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'repository'), 'repository', '__httpmomotor_org1_0_checkletComplexType_httpmomotor_org1_0repository', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 111, 12), )

    
    repository = property(__repository.value, __repository.set, None, None)

    
    # Element {http://momotor.org/1.0}link uses Python identifier link
    __link = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'link'), 'link', '__httpmomotor_org1_0_checkletComplexType_httpmomotor_org1_0link', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 118, 12), )

    
    link = property(__link.value, __link.set, None, None)

    
    # Element {http://momotor.org/1.0}index uses Python identifier index
    __index = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'index'), 'index', '__httpmomotor_org1_0_checkletComplexType_httpmomotor_org1_0index', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 119, 12), )

    
    index = property(__index.value, __index.set, None, None)

    
    # Element {http://momotor.org/1.0}package-version uses Python identifier package_version
    __package_version = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'package-version'), 'package_version', '__httpmomotor_org1_0_checkletComplexType_httpmomotor_org1_0package_version', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 120, 12), )

    
    package_version = property(__package_version.value, __package_version.set, None, None)

    
    # Element {http://momotor.org/1.0}resources uses Python identifier resources
    __resources = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'resources'), 'resources', '__httpmomotor_org1_0_checkletComplexType_httpmomotor_org1_0resources', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 126, 12), )

    
    resources = property(__resources.value, __resources.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_checkletComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_checkletComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_checkletComplexType_name', pyxb.binding.datatypes.string)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 129, 8)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 129, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute extras uses Python identifier extras
    __extras = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'extras'), 'extras', '__httpmomotor_org1_0_checkletComplexType_extras', pyxb.binding.datatypes.string)
    __extras._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 130, 8)
    __extras._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 130, 8)
    
    extras = property(__extras.value, __extras.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpmomotor_org1_0_checkletComplexType_version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 131, 8)
    __version._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 131, 8)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute entrypoint uses Python identifier entrypoint
    __entrypoint = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'entrypoint'), 'entrypoint', '__httpmomotor_org1_0_checkletComplexType_entrypoint', pyxb.binding.datatypes.string)
    __entrypoint._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 132, 8)
    __entrypoint._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 132, 8)
    
    entrypoint = property(__entrypoint.value, __entrypoint.set, None, None)

    _ElementMap.update({
        __repository.name() : __repository,
        __link.name() : __link,
        __index.name() : __index,
        __package_version.name() : __package_version,
        __resources.name() : __resources
    })
    _AttributeMap.update({
        __id.name() : __id,
        __ref.name() : __ref,
        __name.name() : __name,
        __extras.name() : __extras,
        __version.name() : __version,
        __entrypoint.name() : __entrypoint
    })
_module_typeBindings.checkletComplexType = checkletComplexType
Namespace.addCategoryObject('typeBinding', 'checkletComplexType', checkletComplexType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 112, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute src uses Python identifier src
    __src = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'src'), 'src', '__httpmomotor_org1_0_CTD_ANON__src', pyxb.binding.datatypes.anyURI, required=True)
    __src._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 113, 20)
    __src._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 113, 20)
    
    src = property(__src.value, __src.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpmomotor_org1_0_CTD_ANON__type', pyxb.binding.datatypes.string, required=True)
    __type._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 114, 20)
    __type._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 114, 20)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute revision uses Python identifier revision
    __revision = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'revision'), 'revision', '__httpmomotor_org1_0_CTD_ANON__revision', pyxb.binding.datatypes.string)
    __revision._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 115, 20)
    __revision._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 115, 20)
    
    revision = property(__revision.value, __revision.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __src.name() : __src,
        __type.name() : __type,
        __revision.name() : __revision
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 121, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_CTD_ANON_2_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 122, 20)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 122, 20)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'version'), 'version', '__httpmomotor_org1_0_CTD_ANON_2_version', pyxb.binding.datatypes.string)
    __version._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 123, 20)
    __version._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 123, 20)
    
    version = property(__version.value, __version.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __name.name() : __name,
        __version.name() : __version
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type {http://momotor.org/1.0}propertiesComplexType with content type ELEMENT_ONLY
class propertiesComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}propertiesComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'propertiesComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 135, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}property uses Python identifier property_
    __property = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'property'), 'property_', '__httpmomotor_org1_0_propertiesComplexType_httpmomotor_org1_0property', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 137, 12), )

    
    property_ = property(__property.value, __property.set, None, None)

    _ElementMap.update({
        __property.name() : __property
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.propertiesComplexType = propertiesComplexType
Namespace.addCategoryObject('typeBinding', 'propertiesComplexType', propertiesComplexType)


# Complex type {http://momotor.org/1.0}configComplexType with content type ELEMENT_ONLY
class configComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}configComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'configComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 175, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_configComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 177, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_configComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 178, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_configComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 179, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_configComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 181, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 181, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __options.name() : __options,
        __files.name() : __files
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.configComplexType = configComplexType
Namespace.addCategoryObject('typeBinding', 'configComplexType', configComplexType)


# Complex type {http://momotor.org/1.0}productComplexType with content type ELEMENT_ONLY
class productComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}productComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'productComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 184, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_productComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 186, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_productComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 187, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_productComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 188, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_productComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 190, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 190, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __options.name() : __options,
        __files.name() : __files
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.productComplexType = productComplexType
Namespace.addCategoryObject('typeBinding', 'productComplexType', productComplexType)


# Complex type {http://momotor.org/1.0}recipeComplexType with content type ELEMENT_ONLY
class recipeComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}recipeComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'recipeComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 193, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 195, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 196, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}checklets uses Python identifier checklets
    __checklets = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklets'), 'checklets', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0checklets', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 197, 12), )

    
    checklets = property(__checklets.value, __checklets.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 198, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Element {http://momotor.org/1.0}steps uses Python identifier steps
    __steps = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'steps'), 'steps', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0steps', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 199, 12), )

    
    steps = property(__steps.value, __steps.set, None, None)

    
    # Element {http://momotor.org/1.0}tests uses Python identifier tests
    __tests = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'tests'), 'tests', '__httpmomotor_org1_0_recipeComplexType_httpmomotor_org1_0tests', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 200, 12), )

    
    tests = property(__tests.value, __tests.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_recipeComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 202, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 202, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __options.name() : __options,
        __checklets.name() : __checklets,
        __files.name() : __files,
        __steps.name() : __steps,
        __tests.name() : __tests
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.recipeComplexType = recipeComplexType
Namespace.addCategoryObject('typeBinding', 'recipeComplexType', recipeComplexType)


# Complex type {http://momotor.org/1.0}stepsComplexType with content type ELEMENT_ONLY
class stepsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}stepsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'stepsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 205, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}step uses Python identifier step
    __step = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'step'), 'step', '__httpmomotor_org1_0_stepsComplexType_httpmomotor_org1_0step', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 207, 12), )

    
    step = property(__step.value, __step.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_stepsComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 208, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}checklets uses Python identifier checklets
    __checklets = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklets'), 'checklets', '__httpmomotor_org1_0_stepsComplexType_httpmomotor_org1_0checklets', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 209, 12), )

    
    checklets = property(__checklets.value, __checklets.set, None, None)

    _ElementMap.update({
        __step.name() : __step,
        __options.name() : __options,
        __checklets.name() : __checklets
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.stepsComplexType = stepsComplexType
Namespace.addCategoryObject('typeBinding', 'stepsComplexType', stepsComplexType)


# Complex type {http://momotor.org/1.0}dependenciesComplexType with content type ELEMENT_ONLY
class dependenciesComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}dependenciesComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dependenciesComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 236, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}depends uses Python identifier depends
    __depends = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'depends'), 'depends', '__httpmomotor_org1_0_dependenciesComplexType_httpmomotor_org1_0depends', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 238, 12), )

    
    depends = property(__depends.value, __depends.set, None, None)

    _ElementMap.update({
        __depends.name() : __depends
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.dependenciesComplexType = dependenciesComplexType
Namespace.addCategoryObject('typeBinding', 'dependenciesComplexType', dependenciesComplexType)


# Complex type {http://momotor.org/1.0}dependsComplexType with content type ELEMENT_ONLY
class dependsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}dependsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'dependsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 242, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_dependsComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 244, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Attribute step uses Python identifier step
    __step = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'step'), 'step', '__httpmomotor_org1_0_dependsComplexType_step', pyxb.binding.datatypes.IDREF, required=True)
    __step._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 246, 8)
    __step._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 246, 8)
    
    step = property(__step.value, __step.set, None, None)

    _ElementMap.update({
        __options.name() : __options
    })
    _AttributeMap.update({
        __step.name() : __step
    })
_module_typeBindings.dependsComplexType = dependsComplexType
Namespace.addCategoryObject('typeBinding', 'dependsComplexType', dependsComplexType)


# Complex type {http://momotor.org/1.0}testsComplexType with content type ELEMENT_ONLY
class testsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}testsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'testsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 249, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}expectedResult uses Python identifier expectedResult
    __expectedResult = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'expectedResult'), 'expectedResult', '__httpmomotor_org1_0_testsComplexType_httpmomotor_org1_0expectedResult', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 251, 12), )

    
    expectedResult = property(__expectedResult.value, __expectedResult.set, None, None)

    
    # Element {http://momotor.org/1.0}expect uses Python identifier expect
    __expect = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'expect'), 'expect', '__httpmomotor_org1_0_testsComplexType_httpmomotor_org1_0expect', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 252, 12), )

    
    expect = property(__expect.value, __expect.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_testsComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 253, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Element {http://momotor.org/1.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpmomotor_org1_0_testsComplexType_httpmomotor_org1_0properties', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 254, 12), )

    
    properties = property(__properties.value, __properties.set, None, None)

    
    # Element {http://momotor.org/1.0}test uses Python identifier test
    __test = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'test'), 'test', '__httpmomotor_org1_0_testsComplexType_httpmomotor_org1_0test', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 255, 12), )

    
    test = property(__test.value, __test.set, None, None)

    _ElementMap.update({
        __expectedResult.name() : __expectedResult,
        __expect.name() : __expect,
        __files.name() : __files,
        __properties.name() : __properties,
        __test.name() : __test
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.testsComplexType = testsComplexType
Namespace.addCategoryObject('typeBinding', 'testsComplexType', testsComplexType)


# Complex type {http://momotor.org/1.0}testComplexType with content type ELEMENT_ONLY
class testComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}testComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'testComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 259, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_testComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 261, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}product uses Python identifier product
    __product = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'product'), 'product', '__httpmomotor_org1_0_testComplexType_httpmomotor_org1_0product', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 262, 12), )

    
    product = property(__product.value, __product.set, None, None)

    
    # Element {http://momotor.org/1.0}expectedResult uses Python identifier expectedResult
    __expectedResult = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'expectedResult'), 'expectedResult', '__httpmomotor_org1_0_testComplexType_httpmomotor_org1_0expectedResult', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 263, 12), )

    
    expectedResult = property(__expectedResult.value, __expectedResult.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_testComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 265, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 265, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __product.name() : __product,
        __expectedResult.name() : __expectedResult
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.testComplexType = testComplexType
Namespace.addCategoryObject('typeBinding', 'testComplexType', testComplexType)


# Complex type {http://momotor.org/1.0}expectedResultComplexType with content type ELEMENT_ONLY
class expectedResultComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}expectedResultComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'expectedResultComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 268, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}expect uses Python identifier expect
    __expect = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'expect'), 'expect', '__httpmomotor_org1_0_expectedResultComplexType_httpmomotor_org1_0expect', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 270, 12), )

    
    expect = property(__expect.value, __expect.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_expectedResultComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_expectedResultComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    _ElementMap.update({
        __expect.name() : __expect
    })
    _AttributeMap.update({
        __id.name() : __id,
        __ref.name() : __ref
    })
_module_typeBindings.expectedResultComplexType = expectedResultComplexType
Namespace.addCategoryObject('typeBinding', 'expectedResultComplexType', expectedResultComplexType)


# Complex type {http://momotor.org/1.0}resultsComplexType with content type ELEMENT_ONLY
class resultsComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}resultsComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resultsComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 285, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_resultsComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 287, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}checklets uses Python identifier checklets
    __checklets = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklets'), 'checklets', '__httpmomotor_org1_0_resultsComplexType_httpmomotor_org1_0checklets', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 288, 12), )

    
    checklets = property(__checklets.value, __checklets.set, None, None)

    
    # Element {http://momotor.org/1.0}result uses Python identifier result
    __result = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'result'), 'result', '__httpmomotor_org1_0_resultsComplexType_httpmomotor_org1_0result', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 289, 12), )

    
    result = property(__result.value, __result.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_resultsComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 291, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 291, 8)
    
    id = property(__id.value, __id.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __checklets.name() : __checklets,
        __result.name() : __result
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.resultsComplexType = resultsComplexType
Namespace.addCategoryObject('typeBinding', 'resultsComplexType', resultsComplexType)


# Complex type {http://momotor.org/1.0}testResultComplexType with content type ELEMENT_ONLY
class testResultComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}testResultComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'testResultComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 305, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}results uses Python identifier results
    __results = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'results'), 'results', '__httpmomotor_org1_0_testResultComplexType_httpmomotor_org1_0results', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 307, 12), )

    
    results = property(__results.value, __results.set, None, None)

    _ElementMap.update({
        __results.name() : __results
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.testResultComplexType = testResultComplexType
Namespace.addCategoryObject('typeBinding', 'testResultComplexType', testResultComplexType)


# Complex type {http://momotor.org/1.0}propertyComplexType with content type MIXED
class propertyComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}propertyComplexType with content type MIXED"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'propertyComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 141, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpmomotor_org1_0_propertyComplexType_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    __type._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 12, 8)
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'encoding'), 'encoding', '__httpmomotor_org1_0_propertyComplexType_encoding', pyxb.binding.datatypes.string)
    __encoding._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    __encoding._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 13, 8)
    
    encoding = property(__encoding.value, __encoding.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpmomotor_org1_0_propertyComplexType_name', pyxb.binding.datatypes.string, required=True)
    __name._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 145, 8)
    __name._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 145, 8)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute value uses Python identifier value_
    __value = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpmomotor_org1_0_propertyComplexType_value', pyxb.binding.datatypes.string)
    __value._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 146, 8)
    __value._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 146, 8)
    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute accept uses Python identifier accept
    __accept = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'accept'), 'accept', '__httpmomotor_org1_0_propertyComplexType_accept', _module_typeBindings.STD_ANON)
    __accept._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 147, 8)
    __accept._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 147, 8)
    
    accept = property(__accept.value, __accept.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __type.name() : __type,
        __encoding.name() : __encoding,
        __name.name() : __name,
        __value.name() : __value,
        __accept.name() : __accept
    })
_module_typeBindings.propertyComplexType = propertyComplexType
Namespace.addCategoryObject('typeBinding', 'propertyComplexType', propertyComplexType)


# Complex type {http://momotor.org/1.0}stepComplexType with content type ELEMENT_ONLY
class stepComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}stepComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'stepComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 213, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}meta uses Python identifier meta
    __meta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'meta'), 'meta', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0meta', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 215, 12), )

    
    meta = property(__meta.value, __meta.set, None, None)

    
    # Element {http://momotor.org/1.0}dependencies uses Python identifier dependencies
    __dependencies = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), 'dependencies', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0dependencies', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 216, 12), )

    
    dependencies = property(__dependencies.value, __dependencies.set, None, None)

    
    # Element {http://momotor.org/1.0}checklet uses Python identifier checklet
    __checklet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklet'), 'checklet', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0checklet', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 217, 12), )

    
    checklet = property(__checklet.value, __checklet.set, None, None)

    
    # Element {http://momotor.org/1.0}resources uses Python identifier resources
    __resources = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'resources'), 'resources', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0resources', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 218, 12), )

    
    resources = property(__resources.value, __resources.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 219, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_stepComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 220, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_stepComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_stepComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute priority uses Python identifier priority
    __priority = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'priority'), 'priority', '__httpmomotor_org1_0_stepComplexType_priority', _module_typeBindings.STD_ANON_, unicode_default='default')
    __priority._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 223, 8)
    __priority._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 223, 8)
    
    priority = property(__priority.value, __priority.set, None, None)

    _ElementMap.update({
        __meta.name() : __meta,
        __dependencies.name() : __dependencies,
        __checklet.name() : __checklet,
        __resources.name() : __resources,
        __options.name() : __options,
        __files.name() : __files
    })
    _AttributeMap.update({
        __id.name() : __id,
        __ref.name() : __ref,
        __priority.name() : __priority
    })
_module_typeBindings.stepComplexType = stepComplexType
Namespace.addCategoryObject('typeBinding', 'stepComplexType', stepComplexType)


# Complex type {http://momotor.org/1.0}expectComplexType with content type ELEMENT_ONLY
class expectComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}expectComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'expectComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 275, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpmomotor_org1_0_expectComplexType_httpmomotor_org1_0properties', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 277, 12), )

    
    properties = property(__properties.value, __properties.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_expectComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 278, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpmomotor_org1_0_expectComplexType_id', pyxb.binding.datatypes.ID)
    __id._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    __id._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 17, 8)
    
    id = property(__id.value, __id.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpmomotor_org1_0_expectComplexType_ref', pyxb.binding.datatypes.IDREF)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    __ref._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 18, 8)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute step uses Python identifier step
    __step = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'step'), 'step', '__httpmomotor_org1_0_expectComplexType_step', pyxb.binding.datatypes.IDREF)
    __step._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 281, 8)
    __step._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 281, 8)
    
    step = property(__step.value, __step.set, None, None)

    
    # Attribute outcome uses Python identifier outcome
    __outcome = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'outcome'), 'outcome', '__httpmomotor_org1_0_expectComplexType_outcome', _module_typeBindings.outcomeSimpleType)
    __outcome._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 282, 8)
    __outcome._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 282, 8)
    
    outcome = property(__outcome.value, __outcome.set, None, None)

    _ElementMap.update({
        __properties.name() : __properties,
        __files.name() : __files
    })
    _AttributeMap.update({
        __id.name() : __id,
        __ref.name() : __ref,
        __step.name() : __step,
        __outcome.name() : __outcome
    })
_module_typeBindings.expectComplexType = expectComplexType
Namespace.addCategoryObject('typeBinding', 'expectComplexType', expectComplexType)


# Complex type {http://momotor.org/1.0}resultComplexType with content type ELEMENT_ONLY
class resultComplexType (pyxb.binding.basis.complexTypeDefinition):
    """Complex type {http://momotor.org/1.0}resultComplexType with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'resultComplexType')
    _XSDLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 294, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://momotor.org/1.0}checklet uses Python identifier checklet
    __checklet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'checklet'), 'checklet', '__httpmomotor_org1_0_resultComplexType_httpmomotor_org1_0checklet', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 296, 12), )

    
    checklet = property(__checklet.value, __checklet.set, None, None)

    
    # Element {http://momotor.org/1.0}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'properties'), 'properties', '__httpmomotor_org1_0_resultComplexType_httpmomotor_org1_0properties', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 297, 12), )

    
    properties = property(__properties.value, __properties.set, None, None)

    
    # Element {http://momotor.org/1.0}options uses Python identifier options
    __options = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'options'), 'options', '__httpmomotor_org1_0_resultComplexType_httpmomotor_org1_0options', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 298, 12), )

    
    options = property(__options.value, __options.set, None, None)

    
    # Element {http://momotor.org/1.0}files uses Python identifier files
    __files = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'files'), 'files', '__httpmomotor_org1_0_resultComplexType_httpmomotor_org1_0files', True, pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 299, 12), )

    
    files = property(__files.value, __files.set, None, None)

    
    # Attribute step uses Python identifier step
    __step = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'step'), 'step', '__httpmomotor_org1_0_resultComplexType_step', pyxb.binding.datatypes.IDREF, required=True)
    __step._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 301, 8)
    __step._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 301, 8)
    
    step = property(__step.value, __step.set, None, None)

    
    # Attribute outcome uses Python identifier outcome
    __outcome = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'outcome'), 'outcome', '__httpmomotor_org1_0_resultComplexType_outcome', _module_typeBindings.outcomeSimpleType, required=True)
    __outcome._DeclarationLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 302, 8)
    __outcome._UseLocation = pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 302, 8)
    
    outcome = property(__outcome.value, __outcome.set, None, None)

    _ElementMap.update({
        __checklet.name() : __checklet,
        __properties.name() : __properties,
        __options.name() : __options,
        __files.name() : __files
    })
    _AttributeMap.update({
        __step.name() : __step,
        __outcome.name() : __outcome
    })
_module_typeBindings.resultComplexType = resultComplexType
Namespace.addCategoryObject('typeBinding', 'resultComplexType', resultComplexType)


config = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'config'), configComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 311, 4))
Namespace.addCategoryObject('elementBinding', config.name().localName(), config)

product = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'product'), productComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 312, 4))
Namespace.addCategoryObject('elementBinding', product.name().localName(), product)

recipe = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'recipe'), recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 313, 4))
Namespace.addCategoryObject('elementBinding', recipe.name().localName(), recipe)

results = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'results'), resultsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 315, 4))
Namespace.addCategoryObject('elementBinding', results.name().localName(), results)

testresult = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'testresult'), testResultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 316, 4))
Namespace.addCategoryObject('elementBinding', testresult.name().localName(), testresult)

result = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'result'), resultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 314, 4))
Namespace.addCategoryObject('elementBinding', result.name().localName(), result)



metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), pyxb.binding.datatypes.string, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 27, 12)))

metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'version'), pyxb.binding.datatypes.string, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 28, 12)))

metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'author'), pyxb.binding.datatypes.string, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 29, 12)))

metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'description'), CTD_ANON, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 30, 12)))

metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'source'), pyxb.binding.datatypes.anyURI, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 41, 12)))

metaComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'generator'), pyxb.binding.datatypes.string, scope=metaComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 42, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 26, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 27, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'version')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 28, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'author')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 29, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'description')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 30, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'source')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 41, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(metaComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'generator')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 42, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
metaComplexType._Automaton = _BuildAutomaton()




def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 32, 20))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 33, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




optionsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'option'), optionComplexType, scope=optionsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 48, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 47, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(optionsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'option')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 48, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
optionsComplexType._Automaton = _BuildAutomaton_2()




def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 54, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 55, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
optionComplexType._Automaton = _BuildAutomaton_3()




filesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'file'), fileComplexType, scope=filesComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 69, 12)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 68, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 69, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(filesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 69, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
filesComplexType._Automaton = _BuildAutomaton_4()




def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 77, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 78, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
fileComplexType._Automaton = _BuildAutomaton_5()




def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 89, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 90, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
resourceComplexType._Automaton = _BuildAutomaton_6()




resourcesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'resource'), resourceComplexType, scope=resourcesComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 98, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 97, 8))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 98, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(resourcesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'resource')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 98, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True),
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
resourcesComplexType._Automaton = _BuildAutomaton_7()




checkletsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklet'), checkletComplexType, scope=checkletsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 104, 12)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 103, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklet')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 104, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
checkletsComplexType._Automaton = _BuildAutomaton_8()




checkletComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'repository'), CTD_ANON_, scope=checkletComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 111, 12)))

checkletComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'link'), linkComplexType, scope=checkletComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 118, 12)))

checkletComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'index'), linkComplexType, scope=checkletComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 119, 12)))

checkletComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'package-version'), CTD_ANON_2, scope=checkletComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 120, 12)))

checkletComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'resources'), resourcesComplexType, scope=checkletComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 126, 12)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 110, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'repository')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 111, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'link')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 118, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'index')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 119, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'package-version')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 120, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(checkletComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'resources')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 126, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
checkletComplexType._Automaton = _BuildAutomaton_9()




propertiesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'property'), propertyComplexType, scope=propertiesComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 137, 12)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 136, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(propertiesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'property')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 137, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
propertiesComplexType._Automaton = _BuildAutomaton_10()




configComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=configComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 177, 12)))

configComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=configComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 178, 12)))

configComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=configComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 179, 12)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 176, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(configComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 177, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(configComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 178, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(configComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 179, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
configComplexType._Automaton = _BuildAutomaton_11()




productComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=productComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 186, 12)))

productComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=productComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 187, 12)))

productComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=productComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 188, 12)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 185, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(productComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 186, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(productComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 187, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(productComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 188, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
productComplexType._Automaton = _BuildAutomaton_12()




recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 195, 12)))

recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 196, 12)))

recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklets'), checkletsComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 197, 12)))

recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 198, 12)))

recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'steps'), stepsComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 199, 12)))

recipeComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'tests'), testsComplexType, scope=recipeComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 200, 12)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 194, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 195, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 196, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklets')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 197, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 198, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'steps')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 199, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(recipeComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'tests')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 200, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
recipeComplexType._Automaton = _BuildAutomaton_13()




stepsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'step'), stepComplexType, scope=stepsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 207, 12)))

stepsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=stepsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 208, 12)))

stepsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklets'), checkletsComplexType, scope=stepsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 209, 12)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 206, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'step')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 207, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 208, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklets')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 209, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
stepsComplexType._Automaton = _BuildAutomaton_14()




dependenciesComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'depends'), dependsComplexType, scope=dependenciesComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 238, 12)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 237, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dependenciesComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'depends')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 238, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
dependenciesComplexType._Automaton = _BuildAutomaton_15()




dependsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=dependsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 244, 12)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 243, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(dependsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 244, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
dependsComplexType._Automaton = _BuildAutomaton_16()




testsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'expectedResult'), expectedResultComplexType, scope=testsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 251, 12)))

testsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'expect'), expectComplexType, scope=testsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 252, 12)))

testsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=testsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 253, 12)))

testsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), propertiesComplexType, scope=testsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 254, 12)))

testsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'test'), testComplexType, scope=testsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 255, 12)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 250, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'expectedResult')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 251, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'expect')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 252, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 253, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 254, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'test')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 255, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
testsComplexType._Automaton = _BuildAutomaton_17()




testComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=testComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 261, 12)))

testComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'product'), productComplexType, scope=testComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 262, 12)))

testComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'expectedResult'), expectedResultComplexType, scope=testComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 263, 12)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 260, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 261, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'product')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 262, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'expectedResult')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 263, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
testComplexType._Automaton = _BuildAutomaton_18()




expectedResultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'expect'), expectComplexType, scope=expectedResultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 270, 12)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 269, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(expectedResultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'expect')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 270, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
expectedResultComplexType._Automaton = _BuildAutomaton_19()




resultsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=resultsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 287, 12)))

resultsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklets'), checkletsComplexType, scope=resultsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 288, 12)))

resultsComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'result'), resultComplexType, scope=resultsComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 289, 12)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 286, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 287, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklets')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 288, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultsComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'result')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 289, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
resultsComplexType._Automaton = _BuildAutomaton_20()




testResultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'results'), resultsComplexType, scope=testResultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 307, 12)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 306, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(testResultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'results')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 307, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
testResultComplexType._Automaton = _BuildAutomaton_21()




def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 142, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 143, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
propertyComplexType._Automaton = _BuildAutomaton_22()




stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'meta'), metaComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 215, 12)))

stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dependencies'), dependenciesComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 216, 12)))

stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklet'), checkletComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 217, 12)))

stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'resources'), resourcesComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 218, 12)))

stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 219, 12)))

stepComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=stepComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 220, 12)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 214, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'meta')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 215, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dependencies')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 216, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklet')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 217, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'resources')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 218, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 219, 12))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(stepComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 220, 12))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
stepComplexType._Automaton = _BuildAutomaton_23()




expectComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), propertiesComplexType, scope=expectComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 277, 12)))

expectComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=expectComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 278, 12)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 276, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(expectComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 277, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(expectComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 278, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
expectComplexType._Automaton = _BuildAutomaton_24()




resultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'checklet'), checkletComplexType, scope=resultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 296, 12)))

resultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'properties'), propertiesComplexType, scope=resultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 297, 12)))

resultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'options'), optionsComplexType, scope=resultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 298, 12)))

resultComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'files'), filesComplexType, scope=resultComplexType, location=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 299, 12)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 295, 8))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'checklet')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 296, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'properties')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 297, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'options')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 298, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(resultComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'files')), pyxb.utils.utility.Location('file:///d:/IdeaProjects/momotorEngine.py3/engine/momotor-bundles/src/momotor/bundles/schema/momotor-1.0.xsd', 299, 12))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
resultComplexType._Automaton = _BuildAutomaton_25()

