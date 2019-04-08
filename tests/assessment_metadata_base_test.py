"""Test nisomix.assessment_metadata_base module functions."""

import pytest
import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.base import _element
from nisomix.utils import RestrictedElementError
from nisomix.assessment_metadata_base import (image_assessment_metadata,
                                              spatial_metrics, color_encoding,
                                              bits_per_sample, color_map,
                                              gray_response, white_point,
                                              primary_chromaticities,
                                              target_data, target_id)


def test_assessment_metadata():
    """
    Test that the element ImageAssessmentMetadata is created correctly
    and that the subelements are properly sorted.
    """

    target = _element('TargetData')
    spatial = _element('SpatialMetrics')
    encoding = _element('ImageColorEncoding')
    mix = image_assessment_metadata(child_elements=[target, spatial, encoding])

    xml_str = ('<mix:ImageAssessmentMetadata xmlns:mix='
               '"http://www.loc.gov/mix/v20">'
               '<mix:SpatialMetrics/><mix:ImageColorEncoding/>'
               '<mix:TargetData/></mix:ImageAssessmentMetadata>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_spatial_metrics():
    """Test that the element SpatialMetrics is created correctly."""

    mix = spatial_metrics(plane='object plane', unit='cm', x_sampling=2,
                          y_sampling=3)

    xml_str = ('<mix:SpatialMetrics xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:samplingFrequencyPlane>object plane'
               '</mix:samplingFrequencyPlane><mix:samplingFrequencyUnit>cm'
               '</mix:samplingFrequencyUnit><mix:xSamplingFrequency>'
               '<mix:numerator>2</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:xSamplingFrequency>'
               '<mix:ySamplingFrequency><mix:numerator>3</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:ySamplingFrequency>'
               '</mix:SpatialMetrics>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


@pytest.mark.parametrize(('plane', 'unit'), [
    ('object plane', 'foo'),
    ('foo', 'cm')])
def test_spatial_metrics_error(plane, unit):
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        spatial_metrics(plane=plane, unit=unit)


def test_color_encoding():
    """
    Test that the element ImageColorEncoding is created correctly
    and that the subelements are properly sorted.
    """

    bits = _element('BitsPerSample')
    cmap = _element('Colormap')
    gray = _element('GrayResponse')
    white = _element('WhitePoint')
    white2 = _element('WhitePoint')
    primary = _element('PrimaryChromaticities')

    mix = color_encoding(
        samples_pixel=3, extra_samples=['range or depth data'],
        child_elements=[white2, bits, gray, white, primary, cmap])

    xml_str = ('<mix:ImageColorEncoding '
               'xmlns:mix="http://www.loc.gov/mix/v20"><mix:BitsPerSample/>'
               '<mix:samplesPerPixel>3</mix:samplesPerPixel><mix:extraSamples>'
               'range or depth data</mix:extraSamples><mix:Colormap/>'
               '<mix:GrayResponse/><mix:WhitePoint/><mix:WhitePoint/>'
               '<mix:PrimaryChromaticities/></mix:ImageColorEncoding>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_color_encoding_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        color_encoding(extra_samples='foo')


def test_color_encoding_listelem():
    """Tests that certain variables work as both lists and strings."""

    mix = color_encoding(extra_samples=[
        "unspecified data",
        "associated alpha data (with pre-multiplied color)"])
    xml_str = ('<mix:ImageColorEncoding '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:extraSamples>unspecified data</mix:extraSamples>'
               '<mix:extraSamples>'
               'associated alpha data (with pre-multiplied color)'
               '</mix:extraSamples>'
               '</mix:ImageColorEncoding>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    mix = color_encoding(extra_samples="unspecified data")
    xml_str = ('<mix:ImageColorEncoding '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:extraSamples>unspecified data</mix:extraSamples>'
               '</mix:ImageColorEncoding>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_bits_per_sample():
    """Test that the element BitsPerSample is created correctly."""

    mix = bits_per_sample(sample_values=[8, 8, 8], sample_unit='integer')

    xml_str = ('<mix:BitsPerSample xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:bitsPerSampleValue>8</mix:bitsPerSampleValue>'
               '<mix:bitsPerSampleValue>8</mix:bitsPerSampleValue>'
               '<mix:bitsPerSampleValue>8</mix:bitsPerSampleValue>'
               '<mix:bitsPerSampleUnit>integer</mix:bitsPerSampleUnit>'
               '</mix:BitsPerSample>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_bits_per_sample_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        bits_per_sample(sample_unit='foo')


def test_bits_per_sample_listelem():
    """Tests that certain variables work as both lists and strings."""

    mix = bits_per_sample(sample_values=["4", "4b"])
    xml_str = ('<mix:BitsPerSample '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:bitsPerSampleValue>4</mix:bitsPerSampleValue>'
               '<mix:bitsPerSampleValue>4b</mix:bitsPerSampleValue>'
               '</mix:BitsPerSample>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    mix = bits_per_sample(sample_values="4")
    xml_str = ('<mix:BitsPerSample xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:bitsPerSampleValue>4</mix:bitsPerSampleValue>'
               '</mix:BitsPerSample>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_color_map():
    """Tests that the element Colormap is created correctly."""

    mix = color_map(reference='foo', embedded='bar')

    xml_str = ('<mix:Colormap xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:colormapReference>foo</mix:colormapReference>'
               '<mix:embeddedColormap>bar</mix:embeddedColormap>'
               '</mix:Colormap>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gray_response():
    """Tests that the element GrayResponse is created correctly."""

    mix = gray_response(curves=[1, 2],
                        unit='Number represents tenths of a unit')

    xml_str = ('<mix:GrayResponse xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:grayResponseCurve>1</mix:grayResponseCurve>'
               '<mix:grayResponseCurve>2</mix:grayResponseCurve>'
               '<mix:grayResponseUnit>Number represents tenths of a unit'
               '</mix:grayResponseUnit></mix:GrayResponse>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gray_response_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        gray_response(unit='foo')


def test_white_point():
    """Tests that the element WhitePoint is created correctly."""

    mix = white_point(x_value=1, y_value=2)

    xml_str = ('<mix:WhitePoint xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:whitePointXValue><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:whitePointXValue>'
               '<mix:whitePointYValue><mix:numerator>2</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:whitePointYValue>'
               '</mix:WhitePoint>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_primary_chromaticities():
    """
    Tests that the element PrimaryChromaticities is created
    correctly.
    """

    mix = primary_chromaticities(red_x=1, red_y=2, green_x=3,
                                 green_y=4, blue_x=5, blue_y=6)

    xml_str = ('<mix:PrimaryChromaticities '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:primaryChromaticitiesRedX><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesRedX>'
               '<mix:primaryChromaticitiesRedY><mix:numerator>2'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesRedY>'
               '<mix:primaryChromaticitiesGreenX><mix:numerator>3'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesGreenX>'
               '<mix:primaryChromaticitiesGreenY><mix:numerator>4'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesGreenY>'
               '<mix:primaryChromaticitiesBlueX><mix:numerator>5'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesBlueX>'
               '<mix:primaryChromaticitiesBlueY><mix:numerator>6'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:primaryChromaticitiesBlueY>'
               '</mix:PrimaryChromaticities>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_target_data():
    """
    Tests that the element TargetData is created correctly
    and that the subelements are properly sorted.
    """

    target = _element('TargetID')
    mix = target_data(target_types='external', external_targets='testing',
                      performance_data='3', child_elements=[target])

    xml_str = ('<mix:TargetData xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:targetType>external</mix:targetType><mix:TargetID/>'
               '<mix:externalTarget>testing</mix:externalTarget>'
               '<mix:performanceData>3</mix:performanceData>'
               '</mix:TargetData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_target_data_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        target_data(target_types='foo')


def test_target_id():
    """Tests that the element TargetID is created correctly."""

    mix = target_id(manufacturer='1', name='2', target_no='3', media='4')

    xml_str = ('<mix:TargetID xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:targetManufacturer>1</mix:targetManufacturer>'
               '<mix:targetName>2</mix:targetName><mix:targetNo>3'
               '</mix:targetNo><mix:targetMedia>4</mix:targetMedia>'
               '</mix:TargetID>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
