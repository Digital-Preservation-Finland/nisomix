"""Functions for reading and generating MIX Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images (ANSI/NISO Z39.87-2006)
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

import lxml.etree as ET
from xml_helpers.utils import xsi_ns
from nisomix.utils import MIX_NS, NAMESPACES


def mix_ImageAssessmentMetadata(samplingFrequencyPlane=None,
                                samplingFrequencyUnit=None,
                                xSamplingFrequency=None,
                                ySamplingFrequency=None,
                                bitsPerSampleValue_elements=None,
                                bitsPerSampleUnit=None, samplesPerPixel=None,
                                extraSamples_elements=None,
                                colormapReference=None, embeddedColormap=None,
                                grayResponseCurve_elements=None,
                                grayResponseUnit=None,
                                WhitePoint_elements=None,
                                PrimaryChromaticities_elements=None,
                                targetType_elements=None,
                                TargetID_elements=None,
                                externalTarget_elements=None,
                                performanceData_elements=None):
    """Returns MIX ImageAssessmentMetadata element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:ImageAssessmentMetadata>
            <mix:SpatialMetrics>
                <mix:samplingFrequencyPlane></mix:samplingFrequencyPlane>
                <mix:samplingFrequencyUnit></mix:samplingFrequencyUnit>
                <mix:xSamplingFrequency></mix:xSamplingFrequency>
                <mix:ySamplingFrequency></mix:ySamplingFrequency>
            </mix:SpatialMetrics>
            <mix:ImageColorEncoding>
                <mix:BitsPerSample>
                    <mix:bitsPerSampleValue></mix:bitsPerSampleValue>
                    <mix:bitsPerSampleUnit></mix:bitsPerSampleUnit>
                </mix:BitsPerSample>
                <mix:samplesPerPixel></mix:samplesPerPixel>
                <mix:extraSamples></mix:extraSamples>
                <mix:Colormap>
                    <mix:colormapReference></mix:colormapReference>
                    <mix:embeddedColormap></mix:embeddedColormap>
                </mix:Colormap>
                <mix:GrayResponse>
                    <mix:grayResponseCurve></mix:grayResponseCurve>
                    <mix:grayResponseUnit></mix:grayResponseUnit>
                </mix:GrayResponse>
                {{ WhitePoint elements }}
                {{ PrimaryChromaticities elements }}

            </mix:ImageColorEncoding>
            <mix:TargetData>
                <mix:targetType></mix:targetType>
                {{ TargetID  elements }}
                <mix:externalTarget></mix:externalTarget>
                <mix:performanceData></mix:performanceData>
            </mix:TargetData>
        </mix:ImageAssessmentMetadata>

    """
    container = _element('ImageAssessmentMetadata')
    mix_SpatialMetrics = _subelement(
        container, 'SpatialMetrics')

    if samplingFrequencyPlane:
        mix_samplingFrequencyPlane = _subelement(
            mix_SpatialMetrics, 'samplingFrequencyPlane')
        mix_samplingFrequencyPlane.text = samplingFrequencyPlane

    if samplingFrequencyUnit:
        mix_samplingFrequencyUnit = _subelement(
            mix_SpatialMetrics, 'samplingFrequencyUnit')
        mix_samplingFrequencyUnit.text = samplingFrequencyUnit

    if xSamplingFrequency:
        mix_xSamplingFrequency = _subelement(
            mix_SpatialMetrics, 'xSamplingFrequency')
        mix_xSamplingFrequency.text = xSamplingFrequency

    if ySamplingFrequency:
        mix_ySamplingFrequency = _subelement(
            mix_SpatialMetrics, 'ySamplingFrequency')
        mix_ySamplingFrequency.text = ySamplingFrequency

    mix_ImageColorEncoding = _subelement(
        container, 'ImageColorEncoding')
    mix_BitsPerSample = _subelement(mix_ImageColorEncoding, 'BitsPerSample')
    if bitsPerSampleValue_elements:
        for element in bitsPerSampleValue_elements:
            mix_bitsPerSampleValue = _subelement(
                mix_BitsPerSample, 'bitsPerSampleValue')
            mix_bitsPerSampleValue.text = element

    mix_bitsPerSampleUnit = _subelement(mix_BitsPerSample, 'bitsPerSampleUnit')
    mix_bitsPerSampleUnit.text = bitsPerSampleUnit

    mix_samplesPerPixel = _subelement(
        mix_ImageColorEncoding, 'samplesPerPixel')
    mix_samplesPerPixel.text = samplesPerPixel

    if extraSamples_elements:
        for element in extraSamples_elements:
            mix_extraSamples = _subelement(
                mix_ImageColorEncoding, 'extraSamples')
            mix_extraSamples.text = element

    mix_Colormap = _subelement(mix_ImageColorEncoding, 'Colormap')
    if colormapReference:
        mix_colormapReference = _subelement(mix_Colormap, 'colormapReference')
        mix_colormapReference.text = colormapReference

    if embeddedColormap:
        mix_embeddedColormap = _subelement(mix_Colormap, 'embeddedColormap')
        mix_embeddedColormap.text = embeddedColormap

    if grayResponseCurve_elements or grayResponseUnit:
        mix_GrayResponse = _subelement(mix_ImageColorEncoding, 'GrayResponse')

    if grayResponseCurve_elements:
        for element in grayResponseCurve_elements:
            mix_grayResponseCurve = _subelement(mix_GrayResponse,
                                                'grayResponseCurve')
            mix_grayResponseCurve.text = element

    if grayResponseUnit:
        mix_grayResponseUnit = _subelement(
            mix_GrayResponse, 'grayResponseUnit')
        mix_grayResponseUnit.text = grayResponseUnit

    if WhitePoint_elements:
        for element in WhitePoint_elements:
            mix_ImageColorEncoding.append(element)

    if PrimaryChromaticities_elements:
        for element in PrimaryChromaticities_elements:
            mix_ImageColorEncoding.append(element)

    if targetType_elements or TargetID_elements or externalTarget_elements or performanceData_elements:
        mix_TargetData = _subelement(container, 'TargetData')

    if targetType_elements:
        for element in targetType_elements:
            mix_targetType = _subelement(mix_TargetData, 'targetType')
            mix_targetType.text = element

    if TargetID_elements:
        for element in TargetID_elements:
            mix_TargetData.append(element)

    if externalTarget_elements:
        for element in externalTarget_elements:
            mix_externalTarget = _subelement(mix_TargetData, 'externalTarget')
            mix_externalTarget.text = element

    if performanceData_elements:
        for element in performanceData_elements:
            mix_performanceData = _subelement(
                mix_TargetData, 'performanceData')
            mix_performanceData.text = element

    return container


def mix_WhitePoint(whitePointXValue=None, whitePointYValue=None):
    """Returns MIX gpsGroup element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:WhitePoint>
            <mix:whitePointXValue></mix:whitePointXValue>
            <mix:whitePointYValue></mix:whitePointYValue>
        </mix:WhitePoint>

    """
    container = _element('WhitePoint')
    mix_whitePointXValue = _subelement(container, 'whitePointXValue')
    mix_whitePointXValue.text = whitePointXValue

    mix_whitePointYValue = _subelement(container, 'whitePointYValue')
    mix_whitePointYValue.text = whitePointYValue

    return container


def mix_PrimaryChromaticities(primaryChromaticitiesRedX=None,
                              primaryChromaticitiesRedY=None,
                              primaryChromaticitiesGreenX=None,
                              primaryChromaticitiesGreenY=None,
                              primaryChromaticitiesBlueX=None,
                              primaryChromaticitiesBlueY=None):
    """Returns MIX PrimaryChromaticities element

    :Schema documentation: Data Dictionary - Technical Metadata for
                           Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:PrimaryChromaticities>
            <mix:primaryChromaticitiesRedX></mix:primaryChromaticitiesRedX>
            <mix:primaryChromaticitiesRedY></mix:primaryChromaticitiesRedY>
            <mix:primaryChromaticitiesGreenX></mix:primaryChromaticitiesGreenX>
            <mix:primaryChromaticitiesGreenY></mix:primaryChromaticitiesGreenY>
            <mix:primaryChromaticitiesBlueX></mix:primaryChromaticitiesBlueX>
            <mix:primaryChromaticitiesBlueY></mix:primaryChromaticitiesBlueY>
        </mix:PrimaryChromaticities>

    """
    container = _element('PrimaryChromaticities')
    mix_primaryChromaticitiesRedX = _subelement(container,
                                                'primaryChromaticitiesRedX')
    mix_primaryChromaticitiesRedX.text = primaryChromaticitiesRedX

    mix_primaryChromaticitiesRedY = _subelement(container,
                                                'primaryChromaticitiesRedY')
    mix_primaryChromaticitiesRedY.text = primaryChromaticitiesRedY

    mix_primaryChromaticitiesGreenX = _subelement(
        container, 'primaryChromaticitiesGreenX')
    mix_primaryChromaticitiesGreenX.text = primaryChromaticitiesGreenX

    mix_primaryChromaticitiesGreenY = _subelement(
        container, 'primaryChromaticitiesGreenY')
    mix_primaryChromaticitiesGreenY.text = primaryChromaticitiesGreenY

    mix_primaryChromaticitiesBlueX = _subelement(container,
                                                 'primaryChromaticitiesBlueX')
    mix_primaryChromaticitiesBlueX.text = primaryChromaticitiesBlueX

    mix_primaryChromaticitiesBlueY = _subelement(container,
                                                 'primaryChromaticitiesBlueY')
    mix_primaryChromaticitiesBlueY.text = primaryChromaticitiesBlueY

    return container


def mix_TargetID(targetManufacturer=None, targetName=None, targetNo=None,
                 targetMedia=None):
    """Returns MIX TargetID element

    :Schema documentation: Data Dictionary - Technical Metadata for
                           Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:TargetID>
            <mix:targetManufacturer></mix:targetManufacturer>
            <mix:targetName></mix:targetName>
            <mix:targetNo></mix:targetNo>
            <mix:targetMedia></mix:targetMedia>
        </mix:TargetID>

    """
    container = _element('TargetID')
    mix_targetManufacturer = _subelement(container, 'targetManufacturer')
    mix_targetManufacturer.text = targetManufacturer

    mix_targetName = _subelement(container, 'targetName')
    mix_targetName.text = targetName

    mix_targetNo = _subelement(container, 'targetNo')
    mix_targetNo.text = targetNo

    mix_targetMedia = _subelement(container, 'targetMedia')
    mix_targetMedia.text = targetMedia

    return container
