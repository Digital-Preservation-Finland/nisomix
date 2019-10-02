"""Test nisomix.object_information_base module features."""
from __future__ import unicode_literals

import pytest

import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.base import _element
from nisomix.object_information_base import (_normalized_byteorder,
                                             compression,
                                             digital_object_information,
                                             fixity, format_designation,
                                             format_registry, identifier,
                                             parse_message_digest,
                                             parse_object_identifier)
from nisomix.utils import RestrictedElementError


def test_digitalobjectinformation():
    """Test that the element BasicDigitalObjectInformation is
    created correctly and that the elements are sorted as intended.
    """

    compr = compression(compression_scheme='jpeg')
    format_des = format_designation(format_name='jpeg', format_version='1.01')
    ident = _element('ObjectIdentifier')
    format_reg = _element('FormatRegistry')
    fix = _element('Fixity')
    mix = digital_object_information(byte_order='big endian', file_size=1234,
                                     child_elements=[compr, format_des, fix,
                                                     format_reg, ident])

    xml_str = ('<mix:BasicDigitalObjectInformation xmlns:mix='
               '"http://www.loc.gov/mix/v20"><mix:ObjectIdentifier/>'
               '<mix:fileSize>1234</mix:fileSize><mix:FormatDesignation>'
               '<mix:formatName>jpeg</mix:formatName><mix:formatVersion>1.01'
               '</mix:formatVersion></mix:FormatDesignation>'
               '<mix:FormatRegistry/><mix:byteOrder>big endian</mix:byteOrder>'
               '<mix:Compression><mix:compressionScheme>jpeg'
               '</mix:compressionScheme></mix:Compression><mix:Fixity/>'
               '</mix:BasicDigitalObjectInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
    assert mix.xpath('./*')[1].tag == '{http://www.loc.gov/mix/v20}fileSize'
    assert mix.xpath('./*')[2].tag == \
        '{http://www.loc.gov/mix/v20}FormatDesignation'
    assert mix.xpath('./*')[4].tag == '{http://www.loc.gov/mix/v20}byteOrder'
    assert mix.xpath('./*')[5].tag == '{http://www.loc.gov/mix/v20}Compression'


def test_identifier():
    """Test that the element ObjectIdentifier is created correctly."""

    mix_id = identifier(id_type='local', id_value='foo')

    xml_str = ('<mix:ObjectIdentifier xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:objectIdentifierType>local</mix:objectIdentifierType>'
               '<mix:objectIdentifierValue>foo</mix:objectIdentifierValue>'
               '</mix:ObjectIdentifier>')

    assert h.compare_trees(mix_id, ET.fromstring(xml_str))


def test_format_designation():
    """Test that the element FormatDesignation is created correctly."""

    f_des = format_designation(format_name='image/jpeg', format_version='1.01')

    xml_str = ('<mix:FormatDesignation xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:formatName>image/jpeg</mix:formatName>'
               '<mix:formatVersion>1.01</mix:formatVersion>'
               '</mix:FormatDesignation>')

    assert h.compare_trees(f_des, ET.fromstring(xml_str))


def test_format_registry():
    """Test that the element FormatRegistry is created correctly."""

    f_reg = format_registry(registry_name='pronom', registry_key='fmt/43')

    xml_str = ('<mix:FormatRegistry xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:formatRegistryName>pronom</mix:formatRegistryName>'
               '<mix:formatRegistryKey>fmt/43</mix:formatRegistryKey>'
               '</mix:FormatRegistry>')

    assert h.compare_trees(f_reg, ET.fromstring(xml_str))


def test_compression():
    """Test that the element Compression is created correctly."""

    compr = compression(compression_scheme='jpeg', compression_ratio=200)

    xml_str = ('<mix:Compression xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:compressionScheme>jpeg</mix:compressionScheme>'
               '<mix:compressionRatio><mix:numerator>200</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:compressionRatio>'
               '</mix:Compression>')

    assert h.compare_trees(compr, ET.fromstring(xml_str))


def test_compression_local():
    """Test that the element Compression is created correctly."""

    compr = compression(compression_scheme='enumerated in local list',
                        local_value='test', local_list='2')

    xml_str = ('<mix:Compression xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:compressionScheme>enumerated in local list'
               '</mix:compressionScheme><mix:compressionSchemeLocalList>2'
               '</mix:compressionSchemeLocalList>'
               '<mix:compressionSchemeLocalValue>test'
               '</mix:compressionSchemeLocalValue>'
               '</mix:Compression>')

    assert h.compare_trees(compr, ET.fromstring(xml_str))


def test_fixity():
    """Test that the element Fixity is created correctly."""

    fix = fixity(algorithm='MD5', digest='foo', originator='2')

    xml_str = ('<mix:Fixity xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:messageDigestAlgorithm>MD5</mix:messageDigestAlgorithm>'
               '<mix:messageDigest>foo</mix:messageDigest>'
               '<mix:messageDigestOriginator>2</mix:messageDigestOriginator>'
               '</mix:Fixity>')

    assert h.compare_trees(fix, ET.fromstring(xml_str))


def test_fixity_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        fixity(algorithm='foo')


@pytest.mark.parametrize(('input_str', 'expected_output'), [
    ('big endian', 'big endian'),
    ('little endian', 'little endian'),
    ('Little endian', 'little endian'),
    ('big_endian', 'big endian'),
    ('Big-endian (something)', 'big endian'),
    ('foo', None),
    ], ids=['Input "big endian", expected "big endian"',
            'Input "little endian", expected "little endian"',
            'Input "Little endian", expected "little endian"',
            'Input "big_endian", expected "big endian"',
            'Input "Big-endian (something)", expected "big endian"',
            'Input "foo", expected that an exception is raised'])
def test_normalized_byteorder(input_str, expected_output):
    """
    Tests the _normalized_byteorder function by asserting that it outputs
    allowed values from different srings, or raises an exception if it
    couldn't determine the value.
    """
    if expected_output:
        assert _normalized_byteorder(input_str) == expected_output
    else:
        with pytest.raises(RestrictedElementError):
            _normalized_byteorder(input_str)


@pytest.mark.parametrize(('mix_xml', 'fixities'), [
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation><mix:Fixity>'
      '<mix:messageDigestAlgorithm>MD5</mix:messageDigestAlgorithm>'
      '<mix:messageDigest>test</mix:messageDigest></mix:Fixity>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     [('MD5', 'test')]),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '<mix:Fixity />'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     []),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     []),
    (('<mix:Fixity xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:messageDigestAlgorithm />'
      '<mix:messageDigest>test</mix:messageDigest>'
      '</mix:Fixity>'),
     [(None, 'test')]),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '<mix:Fixity>'
      '<mix:messageDigestAlgorithm>MD5</mix:messageDigestAlgorithm>'
      '<mix:messageDigest>test</mix:messageDigest></mix:Fixity>'
      '<mix:Fixity>'
      '<mix:messageDigestAlgorithm>SHA-1</mix:messageDigestAlgorithm>'
      '<mix:messageDigest>test2</mix:messageDigest></mix:Fixity>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     [('MD5', 'test'), ('SHA-1', 'test2')]),
    ], ids=['Fixity container with data',
            'Empty Fixity container',
            'Missing Fixity container',
            'XML root is Fixity container',
            'Multiple Fixity containers'])
def test_parse_message_digest(mix_xml, fixities):
    """
    Tests the parse_message_digest function with test data that
    contains:

        1. A Fixity container with data
        2. An empty Fixity container
        3. The Fixity container missing
        4. The Fixity container and its children directly
        5. Multiple Fixity containers

    The test checks that the function returns the tuple(s) of
    messageDigestAlgorithm and messageDigest correctly.
    """

    mix = ET.fromstring(mix_xml)
    assert parse_message_digest(mix) == fixities


@pytest.mark.parametrize(('mix_xml', 'identifiers'), [
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '<mix:ObjectIdentifier>'
      '<mix:objectIdentifierType>local</mix:objectIdentifierType>'
      '<mix:objectIdentifierValue>1234</mix:objectIdentifierValue>'
      '</mix:ObjectIdentifier>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     [('local', '1234')]),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '<mix:ObjectIdentifier />'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     []),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     []),
    (('<mix:ObjectIdentifier xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:objectIdentifierType>local</mix:objectIdentifierType>'
      '<mix:objectIdentifierValue>1234</mix:objectIdentifierValue>'
      '</mix:ObjectIdentifier>'),
     [('local', '1234')]),
    (('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
      '<mix:BasicDigitalObjectInformation>'
      '<mix:ObjectIdentifier>'
      '<mix:objectIdentifierType>local</mix:objectIdentifierType>'
      '<mix:objectIdentifierValue>1234</mix:objectIdentifierValue>'
      '</mix:ObjectIdentifier>'
      '<mix:ObjectIdentifier>'
      '<mix:objectIdentifierValue>12345</mix:objectIdentifierValue>'
      '</mix:ObjectIdentifier>'
      '</mix:BasicDigitalObjectInformation></mix:mix>'),
     [('local', '1234'), (None, '12345')]),
    ], ids=['ObjectIdentifier container with data',
            'Empty ObjectIdentifier container',
            'Missing ObjectIdentifier container',
            'XML root is ObjectIdentifier container',
            'Multiple ObjectIdentifier containers'])
def test_parse_object_identifier(mix_xml, identifiers):
    """
    Tests the parse_object_identifier function with test data that
    contains:

        1. An ObjectIdentifier container with data
        2. An empty ObjectIdentifier container
        3. The ObjectIdentifier container missing
        4. The ObjectIdentifier container and its children directly
        5. Multiple ObjectIdentifier containers

    The test checks that the function returns the tuple(s) of
    objectIdentifierType and objectIdentifierValue correctly.
    """

    mix = ET.fromstring(mix_xml)
    assert parse_object_identifier(mix) == identifiers
