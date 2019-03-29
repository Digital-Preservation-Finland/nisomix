"""Test nisomix features."""
import pytest
import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.object_information import (digital_object_information, identifier,
                                        compression, format_designation,
                                        format_registry, fixity,
                                        normalized_byteorder, ByteOrderError)


def test_digitalobjectinformation():
    """Test that the element BasicDigitalObjectInformation is
    created correctly and the element are sorted as intended.
    """

    compr = compression(compression_scheme='jpeg')
    format_des = format_designation(format_name='jpeg', format_version='1.01')
    mix = digital_object_information(byte_order='big endian', file_size='1234',
                                     child_elements=[compr, format_des])

    xml_str = ('<mix:BasicDigitalObjectInformation xmlns:mix='
               '"http://www.loc.gov/mix/v20"><mix:fileSize>1234'
               '</mix:fileSize><mix:FormatDesignation><mix:formatName>jpeg'
               '</mix:formatName><mix:formatVersion>1.01</mix:formatVersion>'
               '</mix:FormatDesignation><mix:byteOrder>big endian'
               '</mix:byteOrder><mix:Compression><mix:compressionScheme>jpeg'
               '</mix:compressionScheme></mix:Compression>'
               '</mix:BasicDigitalObjectInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
    assert mix.xpath('./*')[0].tag == '{http://www.loc.gov/mix/v20}fileSize'
    assert mix.xpath('./*')[1].tag == \
        '{http://www.loc.gov/mix/v20}FormatDesignation'
    assert mix.xpath('./*')[2].tag == '{http://www.loc.gov/mix/v20}byteOrder'
    assert mix.xpath('./*')[3].tag == '{http://www.loc.gov/mix/v20}Compression'


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

    compr = compression(compression_scheme='jpeg', compression_ratio='200')

    xml_str = ('<mix:Compression xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:compressionScheme>jpeg</mix:compressionScheme>'
               '<mix:compressionRatio><mix:numerator>200</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:compressionRatio>'
               '</mix:Compression>')

    assert h.compare_trees(compr, ET.fromstring(xml_str))


def test_fixity():
    """Test that the element Fixity is created correctly."""

    fix = fixity(algorithm='md5', digest='foo')

    xml_str = ('<mix:Fixity xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:messageDigestAlgorithm>md5</mix:messageDigestAlgorithm>'
               '<mix:messageDigest>foo</mix:messageDigest>'
               '</mix:Fixity>')

    assert h.compare_trees(fix, ET.fromstring(xml_str))


@pytest.mark.parametrize(('input_str', 'expected_output'), [
    ('big endian', 'big endian'),
    ('little endian', 'little endian'),
    ('Little endian', 'little endian'),
    ('big_endian', 'big endian'),
    ('Big-endian (something)', 'big endian'),
    ('foo', None),
])
def test_normalized_byteorder(input_str, expected_output):
    """
    Tests the normalized_byteorder function by asserting that it outputs
    allowed values from different srings, or raises an exception if it
    couldn't determine the value.
    """
    if expected_output:
        assert normalized_byteorder(input_str) == expected_output
    else:
        with pytest.raises(ByteOrderError):
            normalized_byteorder(input_str)
