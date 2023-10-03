"""
Functions for reading and generating MIX Basic Digital Object
Information metadata and its contents as xml.etree.ElementTree data
structures.

References:
    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
                            Chapter 6: Basic Digital Object Information
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import unicode_literals

from nisomix.base import _element, _rationaltype_element, _subelement, mix_ns
from nisomix.constants import BYTE_ORDER_TYPES, DIGEST_ALGORITHMS
from nisomix.utils import NAMESPACES, RestrictedElementError, basic_do_order

__all__ = ['digital_object_information', 'identifier', 'format_designation',
           'format_registry', 'compression', 'fixity',
           'parse_message_digest', 'parse_object_identifier']


def digital_object_information(byte_order=None, file_size=None,
                               child_elements=None):
    """
    Returns the MIX BasicDigitalObjectInformation element. The
    subelements are sorted according to the order as noted in the
    schema.

    :byte_order: The byte order as a string
    :file_size: The file size in bytes as an integer
    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:BasicDigitalObjectInformation>
          <mix:ObjectIdentifier/>
          <mix:fileSize>1234</mix:fileSize>
          <mix:FormatDesignation/>
          <mix:FormatRegistry/>
          <mix:byteOrder>big endian</mix:byteOrder>
          <mix:Compression/>
          <mix:Fixity/>
        </mix:BasicDigitalObjectInformation>

    """
    if child_elements is None:
        child_elements = []

    container = _element('BasicDigitalObjectInformation')

    if file_size:
        file_size_el = _element('fileSize')
        file_size_el.text = str(file_size)
        child_elements.append(file_size_el)
    if byte_order:
        byte_order_el = _element('byteOrder')
        byte_order_el.text = _normalized_byteorder(byte_order)
        child_elements.append(byte_order_el)

    child_elements.sort(key=basic_do_order)

    for element in child_elements:
        container.append(element)

    return container


def identifier(id_type=None, id_value=None):
    """
    Returns the MIX ObjectIdentifier element.

    :id_type: The identifier type as a string
    :id_value: The identifier value as a string

    Returns the following ElementTree structure::

        <mix:ObjectIdentifier>
          <mix:objectIdentifierType>local</mix:objectIdentifierType>
          <mix:objectIdentifierValue>foo</mix:objectIdentifierValue>
        </mix:ObjectIdentifier>

    """
    container = _element('ObjectIdentifier')

    if id_type:
        id_type_el = _subelement(container, 'objectIdentifierType')
        id_type_el.text = id_type

    if id_value:
        id_value_el = _subelement(container, 'objectIdentifierValue')
        id_value_el.text = id_value

    return container


def format_designation(format_name=None, format_version=None):
    """
    Returns the MIX FormatDesignation element.

    :format_name: The file format name as a string
    :format_version: The file format version as a string

    Returns the following ElementTree structure::

        <mix:FormatDesignation>
          <mix:formatName>image/jpeg</mix:formatName>
          <mix:formatVersion>1.01</mix:formatVersion>
        </mix:FormatDesignation>

    """
    container = _element('FormatDesignation')

    if format_name:
        format_name_el = _subelement(container, 'formatName')
        format_name_el.text = format_name

    if format_version:
        format_version_el = _subelement(container, 'formatVersion')
        format_version_el.text = format_version

    return container


def format_registry(registry_name=None, registry_key=None):
    """
    Returns the MIX FormatRegistry element.

    :registry_name: The file format registry name as a string
    :registry_key: The file format registry key as a string

    Returns the following ElementTree structure::

        <mix:FormatRegistry>
          <mix:formatRegistryName>pronom</mix:formatRegistryName>
          <mix:formatRegistryKey>fmt/43</mix:formatRegistryKey>
        </mix:FormatRegistry>

    """
    container = _element('FormatRegistry')

    if registry_name:
        registry_name_el = _subelement(container, 'formatRegistryName')
        registry_name_el.text = registry_name

    if registry_key:
        registry_key_el = _subelement(container, 'formatRegistryKey')
        registry_key_el.text = registry_key

    return container


def compression(compression_scheme=None, local_list=None,
                local_value=None, compression_ratio=None):
    """
    Returns the MIX Compression element.

    :compression_scheme: The compression scheme as a string
    :local_list: The location of the local enumerated list of
                 compression schemes as a string
    :local_value: The local compression scheme as a string
    :compression_ratio: The compression ratio as a list (or integer)

    Returns the following ElementTree structure::

        <mix:Compression>
            <mix:compressionScheme>
                JPEG 2000 Lossless
            </mix:compressionScheme>
            <mix:compressionSchemeLocalList>
            </mix:compressionSchemeLocalList>
            <mix:compressionSchemeLocalValue>
            </mix:compressionSchemeLocalValue>
            <mix:compressionRatio>
                <mix:numerator>10</mix:numerator>
                <mix:denominator>1</mix:denominator>
            </mix:compressionRatio>
        </mix:Compression>

    """
    container = _element('Compression')

    if compression_scheme:
        compression_scheme_el = _subelement(container, 'compressionScheme')
        compression_scheme_el.text = compression_scheme

    if compression_scheme == 'enumerated in local list':
        local_list_el = _subelement(
            container, 'compressionSchemeLocalList')
        local_list_el.text = local_list
        local_value_el = _subelement(
            container, 'compressionSchemeLocalValue')
        local_value_el.text = local_value

    if compression_ratio:
        _rationaltype_element('compressionRatio', compression_ratio,
                              parent=container)

    return container


def fixity(algorithm=None, digest=None, originator=None):
    """
    Returns the MIX Fixity element.

    :algorithm: The message digest algorithm as a string
    :digest: The message digest as a string
    :originator: The message digest creator agent as a string


    Returns the following ElementTree structure::

        <mix:Fixity>
          <mix:messageDigestAlgorithm>MD5</mix:messageDigestAlgorithm>
          <mix:messageDigest>foo</mix:messageDigest>
          <mix:messageDigestOriginator>foo</mix:messageDigestOriginator>
        </mix:Fixity>

    """
    container = _element('Fixity')

    if algorithm:
        if algorithm in DIGEST_ALGORITHMS:
            algorithm_el = _subelement(container, 'messageDigestAlgorithm')
            algorithm_el.text = algorithm
        else:
            raise RestrictedElementError(
                algorithm, 'messageDigestAlgorithm', DIGEST_ALGORITHMS)

    if digest:
        digest_el = _subelement(container, 'messageDigest')
        digest_el.text = digest

    if originator:
        originator_el = _subelement(container, 'messageDigestOriginator')
        originator_el.text = originator

    return container


def _normalized_byteorder(byte_order):
    """
    Tries to fix the byte_order so that the value corresponds to the
    values allowed in the MIX schema. Normalizes hyphens, underscores
    and capitalized letters. Raises an exception if bytOrder couldn't
    be normalized.

    :byte_order: The input byte order as a string
    :returns: The (fixed) byte order as a string
    """
    byte_order = byte_order.replace('-', ' ').replace('_', ' ')
    byte_order = byte_order.lower()

    if byte_order in BYTE_ORDER_TYPES:
        return byte_order

    if 'big' in byte_order and 'endian' in byte_order:
        return 'big endian'

    if 'little' in byte_order and 'endian' in byte_order:
        return 'little endian'

    raise RestrictedElementError(
        byte_order, 'byteOrder', BYTE_ORDER_TYPES)


def parse_message_digest(elem):
    """
    Returns the message digest algorithm and value from a MIX metadata
    block in XML if the data exists. A mix can contain multiple
    Fixity containers, so the data is returned as a list of
    tuples.

    :elem: An ElementTree strucure
    :returns: A list of tuples of (algorithm, value)
    """
    fixities = []

    if elem.tag != mix_ns('Fixity'):
        try:
            elems = elem.xpath('//mix:Fixity', namespaces=NAMESPACES)
        except IndexError:
            return []

    else:
        elems = [elem]

    for fixity_el in elems:
        algorithm = None
        value = None
        algorithm_el = fixity_el.find('./' + mix_ns('messageDigestAlgorithm'))
        if algorithm_el is not None and algorithm_el.text:
            algorithm = algorithm_el.text
        value_el = fixity_el.find('./' + mix_ns('messageDigest'))
        if value_el is not None and value_el.text:
            value = value_el.text
        if algorithm or value:
            fixities.append((algorithm, value))

    return fixities


def parse_object_identifier(elem):
    """
    Returns the object identifier type and value from a MIX metadata
    block in XML if the data exists. A mix can contain multiple
    ObjectIdentifier containers, so the data is returned as a list of
    tuples.

    :elem: An ElementTree strucure
    :returns: A a list of tuples of (id_type, id_value)
    """
    identifiers = []

    if elem.tag != mix_ns('ObjectIdentifier'):
        try:
            elems = elem.xpath('//mix:ObjectIdentifier',
                               namespaces=NAMESPACES)
        except IndexError:
            return []

    else:
        elems = [elem]

    for id_elem in elems:
        id_type = None
        id_value = None
        id_type_el = id_elem.find('./' + mix_ns('objectIdentifierType'))
        if id_type_el is not None and id_type_el.text:
            id_type = id_type_el.text
        id_value_el = id_elem.find('./' + mix_ns('objectIdentifierValue'))
        if id_value_el is not None and id_value_el.text:
            id_value = id_value_el.text
        if id_type or id_value:
            identifiers.append((id_type, id_value))

    return identifiers
