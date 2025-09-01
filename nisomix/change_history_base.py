"""
Functions for reading and generating MIX Change History metadata and its
contents as xml.etree.ElementTree data structures.

References:
    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
                            Chapter 10: Change History
    * ElementTree
    https://docs.python.org/3.9/library/xml.etree.elementtree.html

"""
from __future__ import annotations

import lxml.etree as ET

from nisomix.base import _element, _ensure_list, _subelement
from nisomix.utils import (
    change_history_order,
    image_processing_order,
    mix_root_order,
)

__all__ = ['change_history',
           'image_processing',
           'previous_image_metadata',
           'processing_software']


def change_history(
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX ChangeHistory element. The subelements are sorted
    according to the order as noted in the schema.

    :param child_elements: Child elements as a list

    :returns:
    The following sorted ElementTree structure::

        <mix:ChangeHistory>
            <mix:ImageProcessing/>
            <mix:PreviousImageMetadata/>
        </mix:ChangeHistory>

    """
    container = _element('ChangeHistory')
    if child_elements:
        child_elements.sort(key=change_history_order)

        for element in child_elements:
            container.append(element)

    return container


# pylint: disable=too-many-arguments
def image_processing(
    datetime: str | None = None,
    source_data: str | None = None,
    agencies: str | list[str] | None = None,
    rationale: str | None = None,
    actions: str | list[str] | None = None,
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX ImageProcessing element.

    :param datetime: The image processing datetime as a string
    :param source_data: The location of source image data as a string
    :param agencies: The processing agencies as a list (or string)
    :param rationale: The rationale for image processing as a string
    :param actions: The image processing steps as a list
    :param child_elements: Child elements as a list

    :returns:
    The following ElementTree structure::

        <mix:ImageProcessing>
            <mix:dateTimeProcessed>2019</mix:dateTimeProcessed>
            <mix:sourceData>foo</mix:sourceData>
            <mix:processingAgency>acme</mix:processingAgency>
            <mix:processingRationale>test</mix:processingRationale>
            <mix:ProcessingSoftware>mysoftware</mix:ProcessingSoftware>
            <mix:processingActions>rotate</mix:processingActions>
        </mix:ImageProcessing>

    """
    container = _element('ImageProcessing')

    if child_elements is None:
        child_elements = []

    if datetime:
        datetime_el = _element('dateTimeProcessed')
        datetime_el.text = datetime
        child_elements.append(datetime_el)

    if source_data:
        source_data_el = _element('sourceData')
        source_data_el.text = source_data
        child_elements.append(source_data_el)

    if agencies:
        agencies = _ensure_list(agencies)
        for item in agencies:
            agency_el = _element('processingAgency')
            agency_el.text = item
            child_elements.append(agency_el)

    if rationale:
        rationale_el = _element('processingRationale')
        rationale_el.text = rationale
        child_elements.append(rationale_el)

    if actions:
        actions = _ensure_list(actions)
        for item in actions:
            action_el = _element('processingActions')
            action_el.text = item
            child_elements.append(action_el)

    child_elements.sort(key=image_processing_order)

    for element in child_elements:
        container.append(element)

    return container


def processing_software(
    name: str | None = None,
    version: str | None = None,
    os_name: str | None = None,
    os_version: str | None = None,
) -> ET._Element:
    """
    Returns the MIX ProcessingSoftware element.

    :param name: The processing software name as a string
    :param version: The processing software version as a string
    :param os_name: The operating system name as a string
    :param os_version: The operating system version as a string

    :returns:
    The following ElementTree structure::

        <mix:ProcessingSoftware>
            <mix:processingSoftwareName>
                my software
            </mix:processingSoftwareName>
            <mix:processingsoftwareversion>
                1.0
            </mix:processingsoftwareversion>
            <mix:processingOperatingSystemName>
                CentOS
            </mix:processingOperatingSystemName>
            <mix:processingOperatingSystemVersion>
                7.0
            </mix:processingOperatingSystemVersion>
        </mix:ProcessingSoftware>

    """
    container = _element('ProcessingSoftware')

    if name:
        name_el = _subelement(container, 'processingSoftwareName')
        name_el.text = name

    if version:
        version_el = _subelement(container, 'processingSoftwareVersion')
        version_el.text = version

    if os_name:
        os_name_el = _subelement(container, 'processingOperatingSystemName')
        os_name_el.text = os_name

    if os_version:
        os_version_el = _subelement(container,
                                    'processingOperatingSystemVersion')
        os_version_el.text = os_version

    return container


def previous_image_metadata(
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX PreviousImageMetadata element.

    :param child_elements: Child elements as a list

    :returns:
    The following ElementTree structure::

        <mix:PreviousImageMetadata>
            [child elements]
        </mix:PreviousImageMetadata>

    """
    container = _element('PreviousImageMetadata')

    if child_elements is None:
        child_elements = []

    child_elements.sort(key=mix_root_order)

    for element in child_elements:
        container.append(element)

    return container
