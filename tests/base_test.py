"""Test nisomix features."""
import pytest
import lxml.etree as ET
from nisomix.base import (MIX_NS, mix_ns, mix_mix, _element, _subelement,
                          _rationale_element, _rationale_subelement)


@pytest.mark.parametrize(('tag', 'prefix'), [
    ('first', None),
    ('second', 'myPrefix'),
])
def test_mix_ns(tag, prefix):
    """Test the namespace usage."""
    new_ns = mix_ns(tag, prefix)
    if prefix:
        tag = prefix + tag[0].upper() + tag[1:]
    assert new_ns == '{%s}%s' % (MIX_NS, tag)


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


def test_rationale_element():
    """
    Tests the _rationale_element function by asserting that the
    element was created correctly, that it is containing both the
    numerator and denominator subelements.
    """
    elem = _rationale_element('test', '30')

    assert ET.tostring(elem) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:test>'))


def test_rationale_subelement():
    """
    Tests the _rationale_subelement function by asserting that the
    element was created correctly as a child element of its parent and
    that it is containing both the numerator and denominator subelements.
    """
    elem = _element('test')
    _rationale_subelement(elem, 'subtest', '30')

    assert ET.tostring(elem) == ET.tostring(ET.fromstring(
        '<mix:test xmlns:mix="http://www.loc.gov/mix/v20">'
        '<mix:subtest><mix:numerator>30</mix:numerator>'
        '<mix:denominator>1</mix:denominator></mix:subtest></mix:test>'))


def test_mix():
    """
    Tests that the mix root element is created and tests that the child
    elements in the mix root are sorted properly.
    """
    mix1 = mix_mix()

    assert mix1.xpath('.')[0].tag == '{http://www.loc.gov/mix/v20}mix'
    assert len(mix1) == 0

    child_elems = []
    information = _element('BasicDigitalObjectInformation')
    child_elems.append(information)
    history = _element('ChangeHistory')
    child_elems.append(history)
    capture = _element('ImageCaptureMetadata')
    child_elems.append(capture)

    mix2 = mix_mix(child_elements=child_elems)
    assert len(mix2) == 3
    assert mix2.xpath('./*')[0].tag == \
        '{http://www.loc.gov/mix/v20}BasicDigitalObjectInformation'
    assert mix2.xpath('./*')[1].tag == \
        '{http://www.loc.gov/mix/v20}ImageCaptureMetadata'
    assert mix2.xpath('./*')[2].tag == \
        '{http://www.loc.gov/mix/v20}ChangeHistory'
