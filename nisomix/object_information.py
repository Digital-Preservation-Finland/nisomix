"""Functions for reading and generating MIX
BasicDigitalObjectInformation metadata and its contents.

"""

from nisomix.mix import _element, _subelement
from nisomix.utils import basic_do_order


def digital_object_information(byte_order=None, file_size=None,
                               child_elements=None):
    """Returns MIX BasicDigitalObjectInformation element

    Returns the following sorted ElementTree structure::

        <mix:BasicDigitalObjectInformation>
          {{ Child elements }}
          <mix:fileSize>1234</mix:fileSize>
          {{ Child elements }}
          <mix:byteOrder>big endian</mix:byteOrder>
          {{ Child elements }}
        </mix:BasicDigitalObjectInformation>

    """
    if child_elements is None:
        child_elements = []

    container = _element('BasicDigitalObjectInformation')

    if file_size:
        file_size_el = _element('fileSize')
        file_size_el.text = file_size
        child_elements.append(file_size_el)
    if byte_order:
        byte_order_el = _element('byteOrder')
        byte_order_el.text = byte_order
        child_elements.append(byte_order_el)

    child_elements.sort(key=basic_do_order)

    for element in child_elements:
        container.append(element)

    return container


def identifier(id_type=None, id_value=None):
    """Returns MIX ObjectIdentifier element.

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
    """Returns MIX FormatDesignation element

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
    """Returns MIX FormatRegistry element

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
    """Returns MIX Compression element

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
        compression_ratio_el = _subelement(container, 'compressionRatio')
        numerator = _subelement(compression_ratio_el, 'numerator')
        numerator.text = compression_ratio
        denominator = _subelement(compression_ratio_el, 'denominator')
        denominator.text = '1'

    return container


def fixity(algorithm=None, digest=None, originator=None):
    """Returns MIX Fixity element.

    Returns the following ElementTree structure::

        <mix:Fixity>
          <mix:messageDigestAlgorithm>MD5</mix:messageDigestAlgorithm>
          <mix:messageDigest>foo</mix:messageDigest>
          <mix:messageDigestOriginator>foo</mix:messageDigestOriginator>
        </mix:Fixity>

    """
    container = _element('Fixity')

    if algorithm:
        algorithm_el = _subelement(container, 'messageDigestAlgorithm')
        algorithm_el.text = algorithm

    if digest:
        digest_el = _subelement(container, 'messageDigest')
        digest_el.text = digest

    if originator:
        originator_el = _subelement(container, 'messageDigestOriginator')
        originator_el.text = originator

    return container
