"""Test nisomix.base module functions."""

import pytest
import lxml.etree as ET
from nisomix.base import (MIX_NS, mix_ns, mix, _element, _subelement,
                          _rationaltype_element, _ensure_list)


@pytest.mark.parametrize(('tag', 'prefix'), [
    ('first', None),
    ('second', 'myPrefix'),
])
def test_mix_ns(tag, prefix):
    """Test the namespace usage."""
    new_ns = mix_ns(tag, prefix)
    if prefix:
        tag = prefix + tag[0].upper() + tag[1:]
    assert new_ns == f'{{{MIX_NS}}}{tag}'


def test_element():
    """
    Tests the _element function by asserting that the element is created
    correctly both with and without a prefix. Also tests that the
    correct namespace is used in the element and that the namespace is
    mapped to the intended prefix when serializing the XML to string.
    """
    elem1 = _element('test')
    assert elem1.tag == '{http://www.loc.gov/mix/v20}test'
    assert ET.tostring(elem1) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20"/>'))

    elem2 = _element('test', 'pre')
    assert elem2.tag == '{http://www.loc.gov/mix/v20}preTest'


def test_subelement():
    """
    Tests the _subelement function by asserting that the element was
    created correctly as a child element of its given parent element
    and that the parent element contains the created subelement.
    """
    elem = _element('test')
    subelem = _subelement(elem, 'test', 'pre')

    assert subelem.tag == '{http://www.loc.gov/mix/v20}preTest'
    assert subelem.getparent() == elem
    assert elem.xpath('./*')[0] == subelem
    assert len(elem) == 1
    assert ET.tostring(elem) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:preTest/></mix:test>'))


def test_rationaltype_element():
    """
    Tests the _rationaltype_element function by asserting that the
    element was created correctly, that it is containing both the
    numerator and denominator subelements even though the numerator
    sometimes is missing or is None. Also assert that the rational
    element is a subelement of its parent element if parent argument is
    given.
    """
    elem1 = _rationaltype_element('test', 30)

    assert ET.tostring(elem1) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:test>'))

    elem2 = _rationaltype_element('test', [30, 3])

    assert ET.tostring(elem2) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>3</mix:denominator></mix:test>'))

    elem3 = _rationaltype_element('test', [30, None])

    assert ET.tostring(elem3) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:test>'))

    elem4 = _rationaltype_element('test', [30, ''])

    assert ET.tostring(elem4) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:test>'))

    parent = _element('parent')
    elem5 = _rationaltype_element('test', [30], parent=parent)

    assert ET.tostring(elem5) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:test>'))
    assert elem5.getparent().tag == '{http://www.loc.gov/mix/v20}parent'


@pytest.mark.parametrize(('value', 'length'), [
    ('test', 1),
    (4, 1),
    (['test', 'test2', 'test3'], 3),
    ([4, 5], 2),
])
def test_ensure_list(value, length):
    """Tests the _ensure_list function."""

    list_value = _ensure_list(value)
    assert isinstance(list_value, list)
    assert len(list_value) == length


def test_mix():
    """
    Tests that the mix root element is created and tests that the child
    elements in the mix root are sorted properly.
    """
    mix1 = mix()

    assert mix1.xpath('.')[0].tag == '{http://www.loc.gov/mix/v20}mix'
    assert len(mix1) == 0

    child_elems = []
    information = _element('BasicDigitalObjectInformation')
    child_elems.append(information)
    history = _element('ChangeHistory')
    child_elems.append(history)
    capture = _element('ImageCaptureMetadata')
    child_elems.append(capture)

    mix2 = mix(child_elements=child_elems)
    assert len(mix2) == 3
    assert mix2.xpath('./*')[0].tag == \
        '{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation'
    assert mix2.xpath('./*')[1].tag == \
        '{http://www.loc.gov/mix/v20}ImageCaptureMetadata'
    assert mix2.xpath('./*')[2].tag == \
        '{http://www.loc.gov/mix/v20}ChangeHistory'
