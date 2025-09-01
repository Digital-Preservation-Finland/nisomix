"""
Functions for reading and generating MIX metadata as
xml.etree.ElementTree data structures.

References:

    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
    * ElementTree
    https://docs.python.org/3.9/library/xml.etree.elementtree.html

"""
from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

import lxml.etree as ET
from xml_helpers.utils import xsi_ns

from nisomix.utils import MIX_NS, NAMESPACES, mix_root_order

__all__ = ['mix', 'mix_ns']


def mix_ns(tag: str, prefix: str = "") -> str:
    """Prefix ElementTree tags with MIX namespace.

    object -> {http://www.loc.gov/mix/v20}object

    The prefix parameter is useful for adding prefixes to tags. It
    changes the first letter of the tag to upercase and appends it
    to the prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :param tag: The tag name as string
    :param prefix: Prefix for the tag to be appended to the tag name
        (default="")
    :returns: Tag name with the namespace and prefix appended

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return f'{{{MIX_NS}}}{prefix}{tag}'
    return f'{{{MIX_NS}}}{tag}'


def _element(
    tag: str, prefix: str = "", namespaces: dict[str, str] | None = None
) -> ET._Element:
    """Return lxml Element with MIX namespace. Given namespaces are
    mapped to the given prefixes.

    :param tag: Tagname
    :param prefix: Prefix for the tag (default="")
    :param namespaces: The namespaces and their prefixes as a dict
    :returns: ElementTree element object

    """
    if namespaces is None:
        namespaces = {}
    namespaces['mix'] = MIX_NS
    return ET.Element(mix_ns(tag, prefix), nsmap=namespaces)


def _subelement(
    parent: ET._Element,
    tag: str,
    prefix: str = "",
    namespaces: dict[str, str] | None = None,
) -> ET._Element:
    """Return subelement for the given parent element. Created element
    is appended to parent element Given namespaces are mapped to the
    given prefixes.

    :param parent: Parent element
    :param tag: Element tagname
    :param prefix: Prefix for the tag
    :param ns: The namespaces and their prefixes as a dict
    :returns: Created subelement

    """
    if namespaces is None:
        namespaces = {}
    namespaces['mix'] = MIX_NS
    return ET.SubElement(parent, mix_ns(tag, prefix), nsmap=namespaces)


def _rationaltype_element(
    tag: str,
    value: int | str | Sequence[str | int | None] | None,
    denominator: str = "1",
    parent: ET._Element | None = None,
) -> ET._Element:
    """Return a rational type element. If parent element is given,
    return the rational element as a subelement of the parent.

    Returns the following ElementTree strucure::

        <mix:{{ tag }}>
            <mix:numerator>foo</numerator>
            <mix:denominator>1</denominator>
        </mix:{{ tag }}>

    :param tag: Element tag name
    :param value: Contents of the numerator part of the element, or
        if it is a list, contains both the numerator and denominator
    :param denominator: Contents of the denominator part of the element
    :param parent: The tag name of the parent element

    """
    value_list = _ensure_list(value)
    numerator = str(value_list[0])

    if len(value_list) == 2 and value_list[1]:
        denominator = str(value_list[1])

    elem = _subelement(parent, tag) if parent is not None else _element(tag)
    numerator_el = _subelement(elem, 'numerator')
    numerator_el.text = numerator
    denominator_el = _subelement(elem, 'denominator')
    denominator_el.text = denominator

    return elem


T = TypeVar("T")


def _ensure_list(value: T | list[T]) -> list[T]:
    """
    Converts value if list if it isn't a list already. Used for
    ensuring that repeating elements always are processed as a list
    even if a string or integer value is given.
    """
    if not isinstance(value, list):
        value = [value]

    return value


def mix(
    child_elements: list[ET._Element] | None = None,
    namespaces: dict[str, str] | None = None,
) -> ET._Element:
    """Create MIX Data Dictionary root element.

    :param child_elements: Any elements appended to the MIX dictionary
    :param namespaces: The namespaces and their prefixes as a dict
    :returns:
    The following ElementTree structure::

        <mix:mix
            xmlns:mix="http://www.loc.gov/mix/v20"
            xmlns:xsi="http://www.w3.org/2001/xmlschema-instance"
            xsi:schemalocation="http://www.loc.gov/mix/v20
                                http://www.loc.gov/mix/mix.xsd"/>

    """
    if namespaces is None:
        namespaces = NAMESPACES

    mix_ = _element('mix', namespaces=namespaces)
    mix_.set(
        xsi_ns('schemaLocation'),
        'http://www.loc.gov/mix/v20 '
        'http://www.loc.gov/mix/mix.xsd')

    if child_elements:
        child_elements.sort(key=mix_root_order)
        for element in child_elements:
            mix_.append(element)

    return mix_
