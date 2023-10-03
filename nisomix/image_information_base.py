"""
Functions for reading and generating MIX Basic Image Information
metadata and its contents as xml.etree.ElementTree data strucures.

References:
    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
                            Chapter 7: Basic Image Information
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""
from __future__ import unicode_literals

from nisomix.base import _element, _subelement, _rationaltype_element
from nisomix.constants import (DJVU_FORMATS, YCBCR_SUBSAMPLE_TYPES,
                               YCBCR_POSITIONING_TYPES,
                               COMPONENT_INTERPRETATION_TYPES)
from nisomix.utils import (RestrictedElementError, image_information_order,
                           photom_interpret_order)


__all__ = ['image_information', 'image_characteristics',
           'photometric_interpretation', 'color_profile', 'ycbcr',
           'ref_black_white', 'component', 'format_characteristics',
           'jpeg2000', 'mrsid', 'djvu']


def image_information(child_elements=None):
    """
    Returns the MIX BasicImageInformation element. The
    subelements are sorted according to the order as noted in the
    schema.

    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:BasicImageInformation>
          <mix:BasicImageCharacteristics/>
          <mix:SpecialFormatCharacteristics/>
        </mix:BasicImageInformation>

    """
    container = _element('BasicImageInformation')

    if child_elements:
        child_elements.sort(key=image_information_order)

        for element in child_elements:
            container.append(element)

    return container


def image_characteristics(width=None, height=None,
                          child_elements=None):
    """
    Returns the MIX BasicImageCharacteristics element.

    :width: The image width in pixels as an integer
    :height: The image height in pixels as an integer
    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:BasicImageCharacteristics>
          <mix:imageWidth>20</mix:imageWidth>
          <mix:imageHeight>10</mix:imageHeight>
          <mix:PhotometricInterpretation/>
        </mix:BasicImageCharacteristics>

    """
    container = _element('BasicImageCharacteristics')

    if width:
        width_el = _subelement(container, 'imageWidth')
        width_el.text = str(width)
    if height:
        height_el = _subelement(container, 'imageHeight')
        height_el.text = str(height)
    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def photometric_interpretation(color_space=None, child_elements=None):
    """"
    Returns the MIX PhotometricInterpretation element.

    :color_space: The color space as a string
    :child_elements: Child elements as a list

    Returns the following sorted ElementTree structure::

        <mix:PhotometricInterpretation>
          <mix:colorSpace>RGB</mix:colorSpace>
          <mix:ColorProfile/>
          <mix:YCbCr/>
          <mix:ReferenceBlackWhite/>
        </mix:PhotometricInterpretation>

    """
    container = _element('PhotometricInterpretation')

    if color_space:
        color_space_el = _subelement(container, 'colorSpace')
        color_space_el.text = color_space
    if child_elements:
        child_elements.sort(key=photom_interpret_order)
        for element in child_elements:
            container.append(element)

    return container


# pylint: disable=too-many-arguments
def color_profile(icc_name=None, icc_version=None, icc_uri=None,
                  local_name=None, local_url=None, embedded_profile=None):
    """
    Returns the MIX ColorProfile element and its subelements.

    :icc_name: The name of the used ICC profile as a string
    :icc_version: The version of the used ICC profile as a string
    :icc_uri: The URL/URN of the used ICC profile as a string
    :local_name: The name of the used local color profile as a string
    :local_url: The URL/URN of the used local color profile as a string
    :embedded_profile: The embedded color profile as base64-encoded data

    Returns the following sorted ElementTree structure::

        <mix:ColorProfile>
          <mix:IccProfile>
            <mix:iccProfileName>sRGB</mix:iccProfileName>
            <mix:iccProfileVersion>1</mix:iccProfileVersion>
            <mix:iccProfileURI>http://...</mix:iccProfileURI>
          </mix:IccProfile/>
          <mix:LocalProfile>
            <mix:localProfileName>local RGB</mix:localProfileName>
            <mix:localProfileURL>http://...</mix:localProfileURL>
          </mix:LocalProfile/>
          <mix:embeddedProfile>
            [Base64-encoded data]
          </mix:embeddedProfile>
        </mix:ColorProfile>

    """
    container = _element('ColorProfile')

    if icc_name or icc_version or icc_uri:
        icc_container = _subelement(container, 'IccProfile')
        if icc_name:
            icc_name_el = _subelement(icc_container, 'iccProfileName')
            icc_name_el.text = icc_name
        if icc_version:
            icc_version_el = _subelement(icc_container, 'iccProfileVersion')
            icc_version_el.text = icc_version
        if icc_uri:
            icc_uri_el = _subelement(icc_container, 'iccProfileURI')
            icc_uri_el.text = icc_uri

    if local_name or local_url:
        local_container = _subelement(container, 'LocalProfile')
        if local_name:
            local_name_el = _subelement(local_container, 'localProfileName')
            local_name_el.text = local_name
        if local_url:
            local_url_el = _subelement(local_container, 'localProfileURL')
            local_url_el.text = local_url

    if embedded_profile:
        embedded_profile_el = _subelement(container, 'embeddedProfile')
        embedded_profile_el.text = str(embedded_profile)

    return container


# pylint: disable=too-many-arguments, too-many-branches
def ycbcr(subsample_horiz=None, subsample_vert=None, positioning=None,
          luma_red=None, luma_green=None, luma_blue=None):
    """
    Returns the MIX YCbCr element and its subelements.

    :subsample_horiz: The horizontal subsample factor as a string
    :subsample_vert: The vertical subsample factor as a string
    :positioning: The positions of subsamples as a string
    :luma_red: The red luminance value as a list (or integer)
    :luma_green: The green luminane value as a list (or integer)
    :luma_blue: The blue luminance value as a list (or integer)

    Returns the following sorted ElementTree structure::

        <mix:YCbCr>
          <mix:YCbCrSubSampling>
            <mix:yCbCrSubsampleHoriz>1</mix:yCbCrSubsampleHoriz>
            <mix:yCbCrSubsampleVert>2</mix:yCbCrSubsampleVert>
          </mix:YCbCrSubSampling/>
          <mix:yCbCrPositioning>1</mix:yCbCrPositioning>
          <mix:YCbCrCoefficients>
            <mix:lumaRed>
              <mix:numerator>10</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:lumaRed>
            <mix:lumaGreen>
              <mix:numerator>20</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:lumaGreen>
            <mix:lumaBlue>
              <mix:numerator>30</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:lumaBlue>
          </mix:YCbCrCoefficients/>
        </mix:YCbCr>

    """
    container = _element('YCbCr')

    if subsample_horiz or subsample_vert:
        subsample_container = _subelement(container, 'YCbCrSubSampling')
        if subsample_horiz:
            if subsample_horiz in YCBCR_SUBSAMPLE_TYPES:
                subsample_horiz_el = _subelement(
                    subsample_container, 'yCbCrSubsampleHoriz')
                subsample_horiz_el.text = subsample_horiz
            else:
                raise RestrictedElementError(
                    subsample_horiz, 'yCbCrSubsampleHoriz',
                    YCBCR_SUBSAMPLE_TYPES)
        if subsample_vert:
            if subsample_vert in YCBCR_SUBSAMPLE_TYPES:
                subsample_vert_el = _subelement(
                    subsample_container, 'yCbCrSubsampleVert')
                subsample_vert_el.text = subsample_vert
            else:
                raise RestrictedElementError(
                    subsample_vert, 'yCbCrSubsampleVert',
                    YCBCR_SUBSAMPLE_TYPES)

    if positioning:
        if positioning in YCBCR_POSITIONING_TYPES:
            positioning_el = _subelement(container, 'yCbCrPositioning')
            positioning_el.text = positioning
        else:
            raise RestrictedElementError(
                positioning, 'yCbCrPositioning', YCBCR_POSITIONING_TYPES)

    if luma_red or luma_green or luma_blue:
        luma_container = _subelement(container, 'YCbCrCoefficients')
        if luma_red:
            _rationaltype_element('lumaRed', luma_red, parent=luma_container)
        if luma_green:
            _rationaltype_element('lumaGreen', luma_green,
                                  parent=luma_container)
        if luma_blue:
            _rationaltype_element('lumaBlue', luma_blue, parent=luma_container)

    return container


def ref_black_white(child_elements=None):
    """
    Returns the MIX ReferenceBlackWhite element.

    :child_elements: Child elements as a list

    Returns the following ElementTree structure::

        <mix:ReferenceBlackWhite>
          <mix:Component/>
        </mix:ReferenceBlackWhite>

    """
    container = _element('ReferenceBlackWhite')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def component(c_photometric_interpretation=None, footroom=None,
              headroom=None):
    """
    Returns MIX Component element.

    :c_photometric_interpretation: The component photometric
                                   interpretation type as a string
    :footroom: The footroom as a list (or integer)
    :headroom: The headroom as a list (or integer)

    Returns the following ElementTree structure::

        <mix:Component>
          <mix:componentPhotometricInterpretation>
            R
          </mix:componentPhotometricInterpretation>
          <mix:footroom>
            <mix:numerator>10</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:footroom>
          <mix:headroom>
            <mix:numerator>20</mix:numerator>
            <mix:denominator>1</mix:denominator>
          </mix:headroom>
        </mix:Component>

    """
    container = _element('Component')

    if c_photometric_interpretation:
        if c_photometric_interpretation in COMPONENT_INTERPRETATION_TYPES:
            cpi_el = _subelement(
                container, 'componentPhotometricInterpretation')
            cpi_el.text = c_photometric_interpretation
        else:
            raise RestrictedElementError(
                c_photometric_interpretation,
                'componentPhotometricInterpretation',
                COMPONENT_INTERPRETATION_TYPES)

    if footroom:
        _rationaltype_element('footroom', footroom, parent=container)

    if headroom:
        _rationaltype_element('headroom', headroom, parent=container)

    return container


def format_characteristics(child_elements=None):
    """
    Returns the MIX SpecialFormatCharacteristics element.

    :child_elements: The child elements as a list

    Returns the following ElementTree structure::

        <mix:SpecialFormatCharacteristics>
          <mix:JPEG2000/>
          <mix:MrSID/>
          <mix:Djvu/>
        </mix:SpecialFormatCharacteristics>

    """
    container = _element('SpecialFormatCharacteristics')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


# pylint: disable=too-many-arguments, too-many-locals
def jpeg2000(codec=None, codec_version=None, codestream_profile=None,
             compliance_class=None, tile_width=None, tile_height=None,
             quality_layers=None, resolution_levels=None):
    """
    Returns the MIX JPEG2000 element.

    :codec: The codec name as a string
    :codec_version: The codec version as a string
    :codestream_profile: The codestream profile as a string
    :compliance_class: The compliance class as a string
    :tile_width: The width in pixels of the tiles as an integer
    :tile_height: The height in pixels of the tiles as an integer
    :quality_layers: The number of quality layers as an integer
    :resolution_levels: The number of lower resolution levels as an
                        integer

    Returns the following ElementTree structure::

        <mix:JPEG2000>
          <mix:CodecCompliance>
            <mix:codec></mix:codec>
            <mix:codecVersion></mix:codecVersion>
            <mix:codestreamProfile></mix:codestreamProfile>
            <mix:complianceClass></mix:complianceClass>
          </mix:CodecCompliance>
          <mix:EncodingOptions>
            <mix:Tiles>
              <mix:tileWidth>2</mix:tileWidth>
              <mix:tileHeight>2</mix:tileHeight>
            </mix:Tiles>
            <mix:qualityLayers>10</mix:qualityLayers>
            <mix:resolutionLevels>10</mix:resolutionLevels>
          </mix:EncodingOptions>
        </mix:JPEG2000>

    """
    container = _element('JPEG2000')

    if codec or codec_version or codestream_profile or compliance_class:
        codec_container = _subelement(container, 'CodecCompliance')
        if codec:
            codec_el = _subelement(codec_container, 'codec')
            codec_el.text = codec
        if codec_version:
            codec_version_el = _subelement(codec_container, 'codecVersion')
            codec_version_el.text = codec_version
        if codestream_profile:
            codestream_profile_el = _subelement(
                codec_container, 'codestreamProfile')
            codestream_profile_el.text = codestream_profile
        if compliance_class:
            compliance_class_el = _subelement(
                codec_container, 'complianceClass')
            compliance_class_el.text = compliance_class

    tiles_container = None
    if tile_width or tile_height:
        tiles_container = _element('Tiles')
        if tile_width:
            tile_width_el = _subelement(tiles_container, 'tileWidth')
            tile_width_el.text = str(tile_width)
        if tile_height:
            tile_height_el = _subelement(tiles_container, 'tileHeight')
            tile_height_el.text = str(tile_height)

    if tiles_container is not None or quality_layers or resolution_levels:
        encoding_options = _subelement(container, 'EncodingOptions')
        if tiles_container is not None:
            encoding_options.append(tiles_container)
        if quality_layers:
            quality_layers_el = _subelement(
                encoding_options, 'qualityLayers')
            quality_layers_el.text = str(quality_layers)
        if resolution_levels:
            resolution_levels_el = _subelement(
                encoding_options, 'resolutionLevels')
            resolution_levels_el.text = str(resolution_levels)

    return container


def mrsid(zoom_levels=None):
    """
    Returns the MIX MrSID element.

    :zoom_levels: The number of available zoom levels as an integer

    Returns the following ElementTree structure::

        <mix:MrSID>
          <mix:zoomLevels>3</mix:zoomLevels>
        </mix:MrSID>

    """
    container = _element('MrSID')

    if zoom_levels:
        zoom_levels_el = _subelement(container, 'zoomLevels')
        zoom_levels_el.text = str(zoom_levels)

    return container


def djvu(djvu_format=None):
    """
    Returns the MIX Djvu element. Djvu format supports only a specific
    set of types.

    :djvu_format: The DjVu file format as a string

    Returns the following ElementTree structure::

        <mix:Djvu>
          <mix:djvuFormat>indirect</mix:djvuFormat>
        </mix:Djvu>

    """
    container = _element('Djvu')

    if djvu_format:
        if djvu_format in DJVU_FORMATS:
            djvu_format_el = _subelement(container, 'djvuFormat')
            djvu_format_el.text = djvu_format
        else:
            raise RestrictedElementError(
                djvu_format, 'djvuFormat', DJVU_FORMATS)

    return container
