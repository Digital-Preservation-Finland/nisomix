"""Functions for reading and generating MIX Image Assessment Metadata and
its contents as xml.etree.ElementTree data structures.

References:
    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
                            Chapter 9: Image Assessment Metadata
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

from nisomix.base import (_element, _subelement, _rationaltype_subelement,
                          _ensure_list)
from nisomix.constants import (SAMPLING_FREQUENCY_PLANES,
                               SAMPLING_FREQUENCY_UNITS, BITS_PER_SAMPLE_UNITS,
                               EXTRA_SAMPLES_TYPES, GRAY_RESPONSE_UNITS,
                               TARGET_TYPES)
from nisomix.utils import (RestrictedElementError, assessment_metadata_order,
                           color_encoding_order, target_data_order)


def image_assessment_metadata(child_elements=None):
    """
    Returns the MIX ImageAssessmentMetadata element.

    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:ImageAssessmentMetadata>
          <mix:SpatialMetrics/>
          <mix:ImageColorEncoding/>
          <mix:TargetData/>
        </mix:ImageAssessmentMetadata>

    """
    container = _element('ImageAssessmentMetadata')
    if child_elements:
        child_elements.sort(key=assessment_metadata_order)
        for element in child_elements:
            container.append(element)

    return container


def spatial_metrics(plane=None, unit=None, x_sampling=None, y_sampling=None):
    """
    Returns the MIX SpatialMetrics element.

    :plane: The sampling frequency plane as a string
    :unit: The sampling frequency unit as a string
    :x_sampling: The y sampling frequency as a list (or integer)
    :y_sampling: The x sampling frequency as a list (or integer)

    Returns the following ElementTree structure::

        <mix:SpatialMetrics>
          <mix:samplingFrequencyPlane>
            object plane
          </mix:samplingFrequencyPlane>
          <mix:samplingFrequencyUnit>cm</mix:samplingFrequencyUnit>
          <mix:xSamplingFrequency>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:xSamplingFrequency>
          <mix:ySamplingFrequency>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:ySamplingFrequency>
        </mix:SpatialMetrics>

    """
    container = _element('SpatialMetrics')

    if plane:
        plane_el = _subelement(container, 'samplingFrequencyPlane')
        if plane in SAMPLING_FREQUENCY_PLANES:
            plane_el.text = plane
        else:
            raise RestrictedElementError(
                plane, 'samplingFrequencyPlane', SAMPLING_FREQUENCY_PLANES)

    if unit:
        unit_el = _subelement(container, 'samplingFrequencyUnit')
        if unit in SAMPLING_FREQUENCY_UNITS:
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                unit, 'samplingFrequencyUnit', SAMPLING_FREQUENCY_UNITS)

    if x_sampling:
        _rationaltype_subelement(container, 'xSamplingFrequency', x_sampling)

    if y_sampling:
        _rationaltype_subelement(container, 'ySamplingFrequency', y_sampling)

    return container


def color_encoding(samples_pixel=None, extra_samples=None,
                   child_elements=None):
    """
    Returns the MIX ImageColorEncoding element.

    :samples_pixel: The number of samples per pixel as an integer
    :extra_samples: The types of extra samples as a list
    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:ImageColorEncoding>
          <mix:BitsPerSample/>
          <mix:samplesPerPixel>3</mix:samplesPerPixel>
          <mix:extraSamples>unspecified data</mix:extraSamples>
          <mix:Colormap/>
          <mix:GrayResponse/>
          <mix:WhitePoint/>
          <mix:PrimaryChromaticities/>
        </mix:ImageColorEncoding>

    """
    container = _element('ImageColorEncoding')

    if child_elements is None:
        child_elements = []

    if samples_pixel:
        pixel_el = _element('samplesPerPixel')
        pixel_el.text = str(samples_pixel)
        child_elements.append(pixel_el)

    if extra_samples:
        extra_samples = _ensure_list(extra_samples)
        for item in extra_samples:
            if item in EXTRA_SAMPLES_TYPES:
                samples_el = _element('extraSamples')
                samples_el.text = item
                child_elements.append(samples_el)
            else:
                raise RestrictedElementError(
                    item, 'extraSamples', EXTRA_SAMPLES_TYPES)

    child_elements.sort(key=color_encoding_order)

    for element in child_elements:
        container.append(element)

    return container


def bits_per_sample(sample_values=None, sample_unit=None):
    """
    Returns the MIX BitsPerSample element.

    :sample_values: The bits per sample values as a list
    :sample_unit: The bits per sample unit as a string

    Returns the following ElementTree structure::

        <mix:BitsPerSample>
          <mix:bitsPerSampleValue>8</mix:bitsPerSampleValue>
          <mix:bitsPerSampleUnit>integer</mix:bitsPerSampleUnit>
        </mix:BitsPerSample>

    """
    container = _element('BitsPerSample')

    if sample_values:
        sample_values = _ensure_list(sample_values)
        for item in sample_values:
            value_el = _subelement(container, 'bitsPerSampleValue')
            value_el.text = str(item)

    if sample_unit:
        if sample_unit in BITS_PER_SAMPLE_UNITS:
            unit_el = _subelement(container, 'bitsPerSampleUnit')
            unit_el.text = sample_unit
        else:
            raise RestrictedElementError(
                sample_unit, 'bitsPerSampleUnit', BITS_PER_SAMPLE_UNITS)

    return container


def color_map(reference=None, embedded=None):
    """
    Returns the MIX Colormap element.

    :reference: The location of the referenced color map as a string
    :embedded: The embedded color map as base64-encoded data

    Returns the following ElementTree structure::

        <mix:Colormap>
          <mix:colormapReference>http://foo</mix:colormapReference>
          <mix:embeddedColormap>foo</mix:embeddedColormap>
        </mix:Colormap>

    """
    container = _element('Colormap')

    if reference:
        reference_el = _subelement(container, 'colormapReference')
        reference_el.text = reference

    if embedded:
        embedded_el = _subelement(container, 'embeddedColormap')
        embedded_el.text = str(embedded)

    return container


def gray_response(curves=None, unit=None):
    """
    Returns the MIX GrayResponse element.

    :curves: The optical density of pixels as a list (of integers)
    :unit: The precision recorded in grayResponseCurve

    Returns the following ElementTree structure::

        <mix:GrayResponse>
          <mix:grayResponseCurve>10</mix:grayResponseCurve>
          <mix:grayResponseUnit>
            Number represents tenths of a unit
          </mix:grayResponseUnit>
        </mix:GrayResponse>

    """
    container = _element('GrayResponse')

    if curves:
        curves = _ensure_list(curves)
        for item in curves:
            curve_el = _subelement(container, 'grayResponseCurve')
            curve_el.text = str(item)

    if unit:
        if unit in GRAY_RESPONSE_UNITS:
            unit_el = _subelement(container, 'grayResponseUnit')
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                unit, 'grayResponseUnit', GRAY_RESPONSE_UNITS)

    return container


def white_point(x_value=None, y_value=None):
    """
    Returns the MIX WhitePoint element.

    :x_value: The X value of white point chromaticity as a list
    :y_value: The Y value of white point chromaticity as a list

    Returns the following ElementTree structure::

        <mix:WhitePoint>
          <mix:whitePointXValue>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:whitePointXValue>
          <mix:whitePointYValue>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:whitePointYValue>
        </mix:WhitePoint>

    """
    container = _element('WhitePoint')

    if x_value:
        _rationaltype_subelement(container, 'whitePointXValue', x_value)

    if y_value:
        _rationaltype_subelement(container, 'whitePointYValue', y_value)

    return container


# pylint: disable=too-many-arguments
def primary_chromaticities(red_x=None, red_y=None, green_x=None, green_y=None,
                           blue_x=None, blue_y=None):
    """
    Returns the MIX PrimaryChromaticities element.

    :red_x: The red X value for the chromaticities as a list
    :red_x: The red Y value for the chromaticities as a list
    :red_x: The green X value for the chromaticities as a list
    :red_x: The green Y value for the chromaticities as a list
    :red_x: The blue X value for the chromaticities as a list
    :red_x: The blue Y value for the chromaticities as a list

    Returns the following ElementTree structure::

        <mix:PrimaryChromaticities>
          <mix:primaryChromaticitiesRedX>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesRedX>
          <mix:primaryChromaticitiesRedY>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesRedY>
          <mix:primaryChromaticitiesGreenX>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesGreenX>
          <mix:primaryChromaticitiesGreenY>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesGreenY>
          <mix:primaryChromaticitiesBlueX>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesBlueX>
          <mix:primaryChromaticitiesBlueY>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:primaryChromaticitiesBlueY>
        </mix:PrimaryChromaticities>

    """
    container = _element('PrimaryChromaticities')

    if red_x:
        _rationaltype_subelement(container, 'primaryChromaticitiesRedX', red_x)

    if red_y:
        _rationaltype_subelement(container, 'primaryChromaticitiesRedY', red_y)

    if green_x:
        _rationaltype_subelement(container, 'primaryChromaticitiesGreenX',
                                 green_x)

    if green_y:
        _rationaltype_subelement(container, 'primaryChromaticitiesGreenY',
                                 green_y)

    if blue_x:
        _rationaltype_subelement(container, 'primaryChromaticitiesBlueX',
                                 blue_x)

    if blue_y:
        _rationaltype_subelement(container, 'primaryChromaticitiesBlueY',
                                 blue_y)

    return container


# pylint: disable=too-many-branches
def target_data(target_types=None, external_targets=None,
                performance_data=None, child_elements=None):
    """
    Returns MIX TargetData element.

    :target_types: The target types as a list (or string)
    :external_targets: The locations of external targets as a list
    :performance_data: The location of performance data as a string
    :child_elements: Child elements as a list

    Returns the following ElementTree structure::

        <mix:TargetData>
          <mix:targetType>internal</mix:targetType>
          <mix:TargetID/>
          <mix:externalTarget>http://foo</mix:externalTarget>
          <mix:performanceData>http://foo</mix:performanceData>
        </mix:TargetData>

    """
    container = _element('TargetData')

    if child_elements is None:
        child_elements = []

    if target_types:
        target_types = _ensure_list(target_types)
        for item in target_types:
            if item in TARGET_TYPES:
                type_el = _element('targetType')
                type_el.text = item
                child_elements.append(type_el)
            else:
                raise RestrictedElementError(
                    item, 'targetType', TARGET_TYPES)

    if external_targets:
        external_targets = _ensure_list(external_targets)
        for item in external_targets:
            target_el = _element('externalTarget')
            target_el.text = item
            child_elements.append(target_el)

    if performance_data:
        performance_data = _ensure_list(performance_data)
        for item in performance_data:
            data_el = _element('performanceData')
            data_el.text = item
            child_elements.append(data_el)

    child_elements.sort(key=target_data_order)

    for element in child_elements:
        container.append(element)

    return container


def target_id(manufacturer=None, name=None, target_no=None, media=None):
    """
    Returns MIX TargetID element.

    :manufacturer: The target manufacturer as a  string
    :name: The target name as a string
    :target_no: The target version or number as a string
    :media: The target media as a string

    Returns the following ElementTree structure::

        <mix:TargetID>
          <mix:targetManufacturer>acme</mix:targetManufacturer>
          <mix:targetName>my target</mix:targetName>
          <mix:targetNo>1.0</mix:targetNo>
          <mix:targetMedia>foo</mix:targetMedia>
        </mix:TargetID>

    """
    container = _element('TargetID')

    if manufacturer:
        manufacturer_el = _subelement(container, 'targetManufacturer')
        manufacturer_el.text = manufacturer

    if name:
        name_el = _subelement(container, 'targetName')
        name_el.text = name

    if target_no:
        target_no_el = _subelement(container, 'targetNo')
        target_no_el.text = target_no

    if media:
        media_el = _subelement(container, 'targetMedia')
        media_el.text = media

    return container
