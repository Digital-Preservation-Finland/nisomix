"""Functions for reading and generating MIX Data Dictionaries as
xml.etree.ElementTree data structures.

"""

from nisomix.base import _element, _subelement, _rationaltype_subelement
from nisomix.utils import (SAMPLING_FREQUENCY_PLANES, SAMPLING_FREQUENCY_UNITS,
                           BITS_PER_SAMPLE_UNITS, EXTRA_SAMPLES_TYPES,
                           GRAY_RESPONSE_UNITS, TARGET_TYPES,
                           RestrictedElementError, assessment_metadata_order,
                           color_encoding_order, target_data_order)


def image_assessment_metadata(child_elements=None):
    """Returns the MIX ImageAssessmentMetadata element."""

    container = _element('ImageAssessmentMetadata')
    if child_elements:
        child_elements.sort(key=assessment_metadata_order)
        for element in child_elements:
            container.append(element)

    return container


def spatial_metrics(plane=None, unit=None, x_sampling=None, y_sampling=None):
    """Returns the MIX SpatialMetrics element."""

    container = _element('SpatialMetrics')

    if plane:
        if plane in SAMPLING_FREQUENCY_PLANES:
            plane_el = _subelement(container, 'samplingFrequencyPlane')
            plane_el.text = plane
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for samplingFrequencyPlane, '
                'accepted values are: "%s".' % (
                    plane, '", "'.join(SAMPLING_FREQUENCY_PLANES)))

    if unit:
        if unit in SAMPLING_FREQUENCY_UNITS:
            unit_el = _subelement(container, 'samplingFrequencyUnit')
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for samplingFrequencyUnit, '
                'accepted values are: "%s".' % (
                    unit, '", "'.join(SAMPLING_FREQUENCY_UNITS)))

    if x_sampling:
        _rationaltype_subelement(container, 'xSamplingFrequency', x_sampling)

    if y_sampling:
        _rationaltype_subelement(container, 'ySamplingFrequency', y_sampling)

    return container


def color_encoding(samples_pixel=None, extra_samples=None,
                   child_elements=None):
    """Returns the MIX ImageColorEncoding element."""
    container = _element('ImageColorEncoding')

    if not child_elements:
        child_elements = []

    if samples_pixel:
        pixel_el = _element('samplesPerPixel')
        pixel_el.text = samples_pixel
        child_elements.append(pixel_el)

    if extra_samples:
        if not isinstance(extra_samples, list):
            extra_samples = [extra_samples]
        for item in extra_samples:
            if item in EXTRA_SAMPLES_TYPES:
                samples_el = _element('extraSamples')
                samples_el.text = item
                child_elements.append(samples_el)
            else:
                raise RestrictedElementError(
                    'The value "%s" is invalid for extraSamples, '
                    'accepted values are: "%s".' % (
                        item, '", "'.join(EXTRA_SAMPLES_TYPES)))

    child_elements.sort(key=color_encoding_order)

    for element in child_elements:
        container.append(element)

    return container


def bits_per_sample(sample_values=None, sample_unit=None):
    """Returns the MIX BitsPerSample element."""
    container = _element('BitsPerSample')

    if sample_values:
        if not isinstance(sample_values, list):
            sample_values = [sample_values]
        for item in sample_values:
            value_el = _subelement(container, 'bitsPerSampleValue')
            value_el.text = item

    if sample_unit:
        if sample_unit in BITS_PER_SAMPLE_UNITS:
            unit_el = _subelement(container, 'bitsPerSampleUnit')
            unit_el.text = sample_unit
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for bitsPerSampleUnit, '
                'accepted values are: "%s".' % (
                    sample_unit, '", "'.join(BITS_PER_SAMPLE_UNITS)))

    return container


def color_map(reference=None, embedded=None):
    """Returns the MIX Colormap element."""
    container = _element('Colormap')

    if reference:
        reference_el = _subelement(container, 'colormapReference')
        reference_el.text = reference

    if embedded:
        embedded_el = _subelement(container, 'embeddedColormap')
        embedded_el.text = embedded

    return container


def gray_response(curves=None, unit=None):
    """Returns the MIX GrayResponse element."""
    container = _element('GrayResponse')

    if curves:
        if not isinstance(curves, list):
            curves = [curves]
        for item in curves:
            curve_el = _subelement(container, 'grayResponseCurve')
            curve_el.text = item

    if unit:
        if unit in GRAY_RESPONSE_UNITS:
            unit_el = _subelement(container, 'grayResponseUnit')
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for grayResponseUnit, '
                'accepted values are: "%s".' % (
                    unit, '", "'.join(GRAY_RESPONSE_UNITS)))

    return container


def white_point(x_value=None, y_value=None):
    """Returns the MIX WhitePoint element."""
    container = _element('WhitePoint')

    if x_value:
        _rationaltype_subelement(container, 'whitePointXValue', x_value)

    if y_value:
        _rationaltype_subelement(container, 'whitePointYValue', y_value)

    return container


# pylint: disable=too-many-arguments
def primary_chromaticities(red_x=None, red_y=None, green_x=None, green_y=None,
                           blue_x=None, blue_y=None):
    """Returns the MIX PrimaryChromaticities element."""
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
    """Returns MIX TargetData element."""
    container = _element('TargetData')

    if not child_elements:
        child_elements = []

    if target_types:
        if not isinstance(target_types, list):
            target_types = [target_types]
        for item in target_types:
            if item in TARGET_TYPES:
                type_el = _element('targetType')
                type_el.text = item
                child_elements.append(type_el)
            else:
                raise RestrictedElementError(
                    'The value "%s" is invalid for targetType, '
                    'accepted values are: "%s".' % (
                        item, '", "'.join(TARGET_TYPES)))

    if external_targets:
        if not isinstance(external_targets, list):
            external_targets = [external_targets]
        for item in external_targets:
            target_el = _element('externalTarget')
            target_el.text = item
            child_elements.append(target_el)

    if performance_data:
        if not isinstance(performance_data, list):
            performance_data = [performance_data]
        for item in performance_data:
            data_el = _element('performanceData')
            data_el.text = item
            child_elements.append(data_el)

    child_elements.sort(key=target_data_order)

    for element in child_elements:
        container.append(element)

    return container


def target_id(manufacturer=None, name=None, target_no=None, media=None):
    """Returns MIX TargetID element."""
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
