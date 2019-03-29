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


def mix_BasicImageInformation(
        imageWidth=None, imageHeight=None, colorSpace=None,
        iccProfileName=None, iccProfileVersion=None, iccProfileURI=None,
        localProfileName=None, localProfileURL=None, embeddedProfile=None,
        yCbCrSubsampleHoriz=None, yCbCrSubsampleVert=None,
        yCbCrPositioning=None, lumaRed=None, lumaGreen=None, lumaBlue=None,
        componentPhotometricInterpretation=None,
        ReferenceBlackWhite_elements=None,
        codec=None, codecVersion=None, codestreamProfile=None,
        complianceClass=None, tileWidth=None, tileHeight=None,
        qualityLayers=None, resolutionLevels=None, zoomLevels=None,
        djvuFormat=None):
    """Returns MIX BasicImageInformation element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:BasicImageInformation>
            <mix:BasicImageCharacteristics>
                <mix:imageWidth>869</mix:imageWidth>
                <mix:imageHeight>1271</mix:imageHeight>
                <mix:PhotometricInterpretation>
                    <mix:colorSpace>ICCBased</<mix:colorSpace>
                    <mix:ColorProfile>
                        <mix:IccProfile>
                            <mix:iccProfileName>Adobe RGB</mix:iccProfileName>
                            <mix:iccProfileVersion>1998</mix:iccProfileVersion>
                            <mix:iccProfileURI>http://www.adobe.com/digitalimag/adobergb.html</mix:iccProfileURI>
                        <mix:IccProfile>
                        <mix:LocalProfile>
                            <mix:localProfileName>xyz</mix:localProfileName>
                            <mix:localProfileURL>http://www.myprofile.com/digitalimag/myrgb.html</mix:localProfileURL>
                        <mix:LocalProfile>
                        <mix:embeddedProfile></mix:embeddedProfile>
                    </mix:ColorProfile>
                    <mix:YCbCr>
                        <mix:YCbCrSubSampling>
                            <mix:yCbCrSubsampleHoriz></mix:yCbCrSubsampleHoriz>
                            <mix:yCbCrSubsampleVert></mix:yCbCrSubsampleVert>
                        </mix:YCbCrSubSampling>
                        <mix:yCbCrPositioning></mix:yCbCrPositioning>
                        <mix:YCbCrCoefficients>
                            <mix:lumaRed></mix:lumaRed>
                            <mix:lumaGreen></mix:lumaGreen>
                            <mix:lumaBlue></mix:lumaBlue>
                        </mix:YCbCrCoefficients>
                    </mix:YCbCr>
                    <mix:ReferenceBlackWhite>
                        <mix:Component>
                            <mix:componentPhotometricInterpretation></mix:componentPhotometricInterpretation>
                            <mix:footroom></mix:footroom>
                            <mix:headroom></mix:headroom>
                        </mix:Component>
                    </mix:ReferenceBlackWhite>
                </mix:PhotometricInterpretation>
            </mix:BasicImageCharacteristics>
            <mix:SpecialFormatCharacteristics>
                <mix:JPEG2000>
                    <mix:CodecCompliance>
                        <mix:codec>Kakadu</mix:codec>
                        <mix:codecVersion>5.2</mix:codecVersion>
                        <mix:codestreamProfile>P1</mix:codestreamProfile>
                        <mix:complianceClass>C1</mix:complianceClass>
                    </mix:CodecCompliance>
                    <mix:EncodingOptions>
                        <mix:Tiles>
                            <mix:tileWidth>256</mix:tileWidth>
                            <mix:tileHeight>256</mix:tileHeight>
                        </mix:Tiles>
                        <mix:qualityLayers></mix:qualityLayers>
                        <mix:resolutionLevels></mix:resolutionLevels>
                    </mix:EncodingOptions>
                </mix:JPEG2000>
                <mix:MrSID>
                    <mix:zoomLevels></mix:zoomLevels>
                </mix:MrSID>
                <mix:Djvu>
                    <mix:djvuFormat></mix:djvuFormat>
                </mix:Djvu>
            </mix:SpecialFormatCharacteristics>

        </mix:BasicImageInformation>

    """

    container = _element('BasicImageInformation')
    mix_BasicImageCharacteristics = _subelement(
        container, 'BasicImageCharacteristics')

    mix_imageWidth = _subelement(mix_BasicImageCharacteristics, 'imageWidth')
    mix_imageWidth.text = imageWidth

    mix_imageHeight = _subelement(mix_BasicImageCharacteristics, 'imageHeight')
    mix_imageHeight.text = imageHeight

    mix_PhotometricInterpretation = _subelement(mix_BasicImageCharacteristics,
                                                'PhotometricInterpretation')

    mix_colorSpace = _subelement(mix_PhotometricInterpretation, 'colorSpace')
    mix_colorSpace.text = colorSpace

    if iccProfileName:
        mix_ColorProfile = _subelement(
            mix_PhotometricInterpretation, 'ColorProfile')
        mix_IccProfile = _subelement(mix_ColorProfile, 'IccProfile')
        mix_iccProfileName = _subelement(mix_IccProfile, 'iccProfileName')
        mix_iccProfileName.text = iccProfileName

    if iccProfileVersion:
        mix_iccProfileVersion = _subelement(
            mix_IccProfile, 'iccProfileVersion')
        mix_iccProfileVersion.text = iccProfileVersion

    if iccProfileURI:
        mix_iccProfileURI = _subelement(mix_IccProfile, 'iccProfileURI')
        mix_iccProfileURI.text = iccProfileURI

    if localProfileName:
        mix_LocalProfile = _subelement(mix_ColorProfile, 'LocalProfile')
        mix_localProfileName = _subelement(
            mix_LocalProfile, 'localProfileName')
        mix_localProfileName.text = localProfileName

        mix_localProfileURL = _subelement(mix_LocalProfile, 'localProfileURL')
        mix_localProfileURL.text = localProfileURL

    if embeddedProfile:
        mix_embeddedProfile = _subelement(mix_ColorProfile, 'embeddedProfile')
        mix_embeddedProfile.text = embeddedProfile

    if yCbCrSubsampleHoriz:
        mix_YCbCr = _subelement(mix_PhotometricInterpretation, 'YCbCr')
        mix_YCbCrSubSampling = _subelement(mix_YCbCr, 'YCbCrSubSampling')
        mix_yCbCrSubsampleHoriz = _subelement(
            mix_YCbCrSubSampling, 'yCbCrSubsampleHoriz')
        mix_yCbCrSubsampleHoriz.text = yCbCrSubsampleHoriz

    if yCbCrSubsampleVert:
        mix_yCbCrSubsampleVert = _subelement(
            mix_YCbCrSubSampling, 'yCbCrSubsampleVert')
        mix_yCbCrSubsampleVert.text = yCbCrSubsampleVert

    if yCbCrPositioning:
        mix_yCbCrPositioning = _subelement(mix_YCbCr, 'yCbCrPositioning')
        mix_yCbCrPositioning.text = yCbCrPositioning

    if lumaRed:
        mix_YCbCrCoefficients = _subelement(mix_YCbCr, 'YCbCrCoefficients')
        mix_lumaRed = _subelement(mix_YCbCrCoefficients, 'lumaRed')
        mix_lumaRed.text = lumaRed

    if lumaGreen:
        mix_lumaGreen = _subelement(mix_YCbCrCoefficients, 'lumaGreen')
        mix_lumaGreen.text = lumaGreen

    if lumaBlue:
        mix_lumaBlue = _subelement(mix_YCbCrCoefficients, 'lumaBlue')
        mix_lumaBlue.text = lumaBlue

    if ReferenceBlackWhite_elements:
        for element in ReferenceBlackWhite_elements:
            mix_PhotometricInterpretation.append(element)

    if any((codec, codecVersion, codestreamProfile, complianceClass, tileWidth,
            tileHeight, qualityLayers, resolutionLevels, zoomLevels,
            djvuFormat)):
        mix_SpecialFormatCharacteristics = _subelement(
            container,
            'SpecialFormatCharacteristics')
    if any((codec, codecVersion, codestreamProfile, complianceClass, tileWidth,
            tileHeight, qualityLayers, resolutionLevels)):
        mix_JPEG2000 = _subelement(
            mix_SpecialFormatCharacteristics, 'JPEG2000')

    if any((codec, codecVersion, codestreamProfile, complianceClass)):
        mix_CodecCompliance = _subelement(mix_JPEG2000, 'CodecCompliance')

    if codec:
        mix_codec = _subelement(mix_CodecCompliance, 'codec')
        mix_codec.text = codec

    if codecVersion:
        mix_codecVersion = _subelement(mix_CodecCompliance, 'codecVersion')
        mix_codecVersion.text = codecVersion

    if codestreamProfile:
        mix_codestreamProfile = _subelement(
            mix_CodecCompliance, 'codestreamProfile')
        mix_codestreamProfile.text = codestreamProfile

    if complianceClass:
        mix_complianceClass = _subelement(
            mix_CodecCompliance, 'complianceClass')
        mix_complianceClass.text = complianceClass

    if tileWidth or tileHeight or qualityLayers or resolutionLevels:
        mix_EncodingOptions = _subelement(mix_JPEG2000, 'EncodingOptions')

    if tileWidth or tileHeight:
        mix_Tiles = _subelement(mix_EncodingOptions, 'Tiles')

    if tileWidth:
        mix_tileWidth = _subelement(mix_Tiles, 'tileWidth')
        mix_tileWidth.text = tileWidth

    if tileHeight:
        mix_tileHeight = _subelement(mix_Tiles, 'tileHeight')
        mix_tileHeight.text = tileHeight

    if qualityLayers:
        mix_qualityLayers = _subelement(mix_EncodingOptions, 'qualityLayers')
        mix_qualityLayers.text = qualityLayers

    if resolutionLevels:
        mix_resolutionLevels = _subelement(
            mix_EncodingOptions, 'resolutionLevels')
        mix_resolutionLevels.text = resolutionLevels

    if zoomLevels:
        mix_MrSID = _subelement(mix_SpecialFormatCharacteristics, 'MrSID')
        mix_zoomLevels = _subelement(mix_MrSID, 'zoomLevels')
        mix_zoomLevels.text = zoomLevels

    if djvuFormat:
        mix_Djvu = _subelement(mix_SpecialFormatCharacteristics, 'Djvu')
        mix_djvuFormat = _subelement(mix_Djvu, 'djvuFormat')
        mix_djvuFormat.text = djvuFormat

    return container


def mix_Component(
        componentPhotometricInterpretation=None, footroom=None, headroom=None):
    """Returns MIX Component element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:Component>
            <mix:componentPhotometricInterpretation></mix:componentPhotometricInterpretation>
            <mix:footroom></mix:footroom>
            <mix:headroom></mix:headroom>
        </mix:Component>

    """

    container = _element('Component')

    cpi_element = _subelement(
        container, 'componentPhotometricInterpretation'
    )
    cpi_element.text = componentPhotometricInterpretation

    mix_footroom = _subelement(container, 'footroom')
    mix_footroom.text = footroom

    mix_headroom = _subelement(container, 'headroom')
    mix_headroom.text = headroom

    return container


def mix_ReferenceBlackWhite(child_elements=None):
    """Returns MIX ReferenceBlackWhite element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)
    :child_elements: Any child elements appended to the ReferenceBlackWhite (default=None)

    Returns the following ElementTree structure::

        <mix:ReferenceBlackWhite>
            {{ child elements }}
        </mix:ReferenceBlackWhite>

    """
    container = _element('ReferenceBlackWhite')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container
