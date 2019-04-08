"""
Functions for reading and generating MIX metadata as
xml.etree.ElementTree data structures.

References:

    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

import lxml.etree as ET
from xml_helpers.utils import xsi_ns
from nisomix.utils import MIX_NS, NAMESPACES, mix_root_order


def mix_ns(tag, prefix=""):
    """Prefix ElementTree tags with MIX namespace.

    object -> {http://www.loc.gov/mix/v20}object

    The prefix parameter is useful for adding prefixes to tags. It
    changes the first letter of the tag to upercase and appends it
    to the prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :tag: The tag name as string
    :prefix: Prefix for the tag to be appended to the tag name
             (default="")
    :returns: Tag name with the namespace and prefix appended

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{%s}%s%s' % (MIX_NS, prefix, tag)
    return '{%s}%s' % (MIX_NS, tag)


def _element(tag, prefix="", namespaces=None):
    """Return lxml Element with MIX namespace. Given namespaces are
    mapped to the given prefixes.

    :tag: Tagname
    :prefix: Prefix for the tag (default="")
    :namespaces: The namespaces and their prefixes as a dict
    :returns: ElementTree element object

    """
    if namespaces is None:
        namespaces = {}
    namespaces['mix'] = MIX_NS
    return ET.Element(mix_ns(tag, prefix), nsmap=namespaces)


def _subelement(parent, tag, prefix="", namespaces=None):
    """Return subelement for the given parent element. Created element
    is appended to parent element Given namespaces are mapped to the
    given prefixes.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :ns: The namespaces and their prefixes as a dict
    :returns: Created subelement

    """
    if namespaces is None:
        namespaces = {}
    namespaces['mix'] = MIX_NS
    return ET.SubElement(parent, mix_ns(tag, prefix), nsmap=namespaces)


def _rationaltype_element(tag, value, denominator='1'):
    """Return a rational type element.

    Returns the following ElementTree strucure::

        <mix:{{ tag }}>
          <mix:numerator>foo</numerator>
          <mix:denominator>1</denominator>
        </mix:{{ tag }}>

    :tag: Element tag name
    :value: Contents of the numerator part of the element, or
            if it is a list, contains both the numerator and denominator
    :denominator: Contents of the denominator part of the element

    """
    value = _ensure_list(value)
    numerator = str(value[0])

    if len(value) == 2:
        denominator = str(value[1])

    elem = _element(tag)
    numerator_el = _subelement(elem, 'numerator')
    numerator_el.text = numerator
    denominator_el = _subelement(elem, 'denominator')
    denominator_el.text = denominator

    return elem


def _rationaltype_subelement(parent, tag, value, denominator='1'):
    """Return a rational type element for the parent.

    Returns the following ElementTree strucure::

        <mix:{{ tag }}>
          <mix:numerator>foo</numerator>
          <mix:denominator>1</denominator>
        </mix:{{ tag }}>

    :parent: Parent element
    :tag: Element tag name
    :value: Contents of the numerator part of the element, or
            if it is a list, contains both the numerator and denominator
    :denominator: Contents of the denominator part of the element

    """
    value = _ensure_list(value)
    numerator = str(value[0])

    if len(value) == 2:
        denominator = str(value[1])

    elem = _subelement(parent, tag)
    numerator_el = _subelement(elem, 'numerator')
    numerator_el.text = numerator
    denominator_el = _subelement(elem, 'denominator')
    denominator_el.text = denominator

    return elem


def _ensure_list(value):
    """
    Converts value if list if it isn't a list already. Used for
    ensuring that repeating elements always are processed as a list
    even if a string or integer value is given.
    """
    if not isinstance(value, list):
        value = [value]

    return value


def mix(child_elements=None, namespaces=None):
    """Create MIX Data Dictionary root element.

    :child_elements: Any elements appended to the MIX dictionary

    Returns the following ElementTree structure::


        <mix:mix
            xmlns:mix="http://www.loc.gov/mix/v20"
            xmlns:xsi="http://www.w3.org/2001/xmlschema-instance"
            xsi:schemalocation="http://www.loc.gov/mix/v20
                                http://www.loc.gov/mix/mix.xsd"/>

    """
    if namespaces is None:
        namespaces = NAMESPACES

    _mix = _element('mix', namespaces=namespaces)
    _mix.set(
        xsi_ns('schemaLocation'),
        'http://www.loc.gov/mix/v20 '
        'http://www.loc.gov/mix/mix.xsd')

    if child_elements:
        child_elements.sort(key=mix_root_order)
        for element in child_elements:
            _mix.append(element)

    return _mix
