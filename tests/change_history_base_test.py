"""Test nisomix.change_history_base module functions."""

import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.base import _element
from nisomix.change_history_base import (change_history,
                                         image_processing,
                                         previous_image_metadata,
                                         processing_software)


def test_change_history():
    """Test that the element ChangeHistory is created correctly and
    that the elements are sorted as intended.
    """

    processing = _element('ImageProcessing')
    prev_metadata = _element('PreviousImageMetadata')
    mix = change_history(child_elements=[prev_metadata, processing])

    xml_str = ('<mix:ChangeHistory xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:ImageProcessing/><mix:PreviousImageMetadata/>'
               '</mix:ChangeHistory>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_processing():
    """Test that the element ImageProcessing is created correctly."""

    processing = _element('ProcessingSoftware')
    mix = image_processing(datetime='2019', source_data='test',
                           agencies=['local', 'external'],
                           rationale='test', actions=['twist', 'shout'],
                           child_elements=[processing])

    xml_str = ('<mix:ImageProcessing xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:dateTimeProcessed>2019</mix:dateTimeProcessed>'
               '<mix:sourceData>test</mix:sourceData><mix:processingAgency>'
               'local</mix:processingAgency><mix:processingAgency>external'
               '</mix:processingAgency><mix:processingRationale>test'
               '</mix:processingRationale><mix:ProcessingSoftware/>'
               '<mix:processingActions>twist</mix:processingActions>'
               '<mix:processingActions>shout</mix:processingActions>'
               '</mix:ImageProcessing>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_processing_listelem():
    """Tests that certain variables work as both lists and strings."""

    mix = image_processing(agencies=['local', 'external'],
                           actions=['twist', 'shout'])

    xml_str = ('<mix:ImageProcessing xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:processingAgency>local</mix:processingAgency>'
               '<mix:processingAgency>external</mix:processingAgency>'
               '<mix:processingActions>twist</mix:processingActions>'
               '<mix:processingActions>shout</mix:processingActions>'
               '</mix:ImageProcessing>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    mix = image_processing(agencies='local', actions='twist')

    xml_str = ('<mix:ImageProcessing xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:processingAgency>local</mix:processingAgency>'
               '<mix:processingActions>twist</mix:processingActions>'
               '</mix:ImageProcessing>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_processing_software():
    """Test that the element ProcessingSoftware is created correctly."""

    mix = processing_software(name='test', version='1.0', os_name='test2',
                              os_version='2.0')

    xml_str = ('<mix:ProcessingSoftware '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:processingSoftwareName>test</mix:processingSoftwareName>'
               '<mix:processingSoftwareVersion>1.0'
               '</mix:processingSoftwareVersion>'
               '<mix:processingOperatingSystemName>test2'
               '</mix:processingOperatingSystemName>'
               '<mix:processingOperatingSystemVersion>2.0'
               '</mix:processingOperatingSystemVersion>'
               '</mix:ProcessingSoftware>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_previous_image_metadata():
    """Test that the element PreviousImageMetadata is created
    correctly.
    """

    processing = _element('BasicDigitalObjectInformation')
    mix = previous_image_metadata(child_elements=[processing])

    xml_str = ('<mix:PreviousImageMetadata '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:BasicDigitalObjectInformation/>'
               '</mix:PreviousImageMetadata>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
