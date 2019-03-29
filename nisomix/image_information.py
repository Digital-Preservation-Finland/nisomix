"""
Functions for reading and generating MIX BasicImageInformatio
metadata and its contents.
"""

from nisomix.mix import _element, _subelement


def image_information(child_elements=None):
    """Creates the MIX BasicImageInformation element."""

    container = _element('BasicImageInformation')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def image_characteristics(width=None, height=None,
                          child_elements=None):
    """Creates the MIX BasicImageCharacteristics element."""

    container = _element('BasicImageCharacteristics')

    if width:
        width_el = _subelement(container, 'imageWidth')
        width_el.text = width
    if height:
        height_el = _subelement(container, 'imageHeight')
        height_el.text = height
    if child_elements:
        container.append(child_elements[0])

    return container


def photometric_interpretation(color_space=None, child_elements=None):
    """"Creates the MIX PhotometricInterpretation element."""

    container = _element('PhotometricInterpretation')
    if color_space:
        color_space_el = _subelement(container, 'colorSpace')
        color_space_el.text = color_space
    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def color_profile(icc_name=None, icc_version=None, icc_uri=None,
                  local_name=None, local_url=None, embedded_profile=None):
    """Creates the MIX ColorProfile element and its subelements."""

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
        embedded_profile_el.text = embedded_profile

    return container


def ycbcr(subsample_horiz=None, subsample_vert=None, positioning=None,
          luma_red=None, luma_green=None, luma_blue=None):
    """Creates the MIX YCbCr element and its subelements."""

    container = _element('YCbCr')

    if subsample_horiz or subsample_vert:
        subsample_container = _subelement(container, 'YCbCrSubSampling')
        if subsample_horiz:
            subsample_horiz_el = _subelement(
                subsample_container, 'yCbCrSubsampleHoriz')
            subsample_horiz_el.text = subsample_horiz
        if subsample_vert:
            subsample_vert_el = _subelement(
                subsample_container, 'yCbCrSubsampleVert')
            subsample_vert_el.text = subsample_vert

    if positioning:
        positioning_el = _subelement(container, 'yCbCrPositioning')
        positioning_el.text = positioning

    if luma_red or luma_green or luma_blue:
        luma_container = _subelement(container, 'YCbCrCoefficients')
        if luma_red:
            luma_red_el = _subelement(luma_container, 'lumaRed')
            numerator = _subelement(luma_red_el, 'numerator')
            numerator.text = luma_red
            denominator = _subelement(luma_red_el, 'denominator')
            denominator.text = '1'
        if luma_green:
            luma_green_el = _subelement(luma_container, 'lumaGreen')
            numerator = _subelement(luma_green_el, 'numerator')
            numerator.text = luma_green
            denominator = _subelement(luma_green_el, 'denominator')
            denominator.text = '1'
        if luma_blue:
            luma_blue_el = _subelement(luma_container, 'lumaBlue')
            numerator = _subelement(luma_blue_el, 'numerator')
            numerator.text = luma_blue
            denominator = _subelement(luma_blue_el, 'denominator')
            denominator.text = '1'

    return container


def ref_black_white(child_elements=None):
    """Creates the MIX ReferenceBlackWhite element."""

    container = _element('ReferenceBlackWhite')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def component(c_photometric_interpretation=None, footroom=None,
              headroom=None):
    """Returns MIX ReferenceBlackWhite element."""

    container = _element('Component')

    if c_photometric_interpretation:
        cpi_el = _subelement(
            container, 'componentPhotometricInterpretation')
        cpi_el.text = c_photometric_interpretation

    if footroom:
        footroom_el = _subelement(container, 'footroom')
        numerator = _subelement(footroom_el, 'numerator')
        numerator.text = footroom
        denominator = _subelement(footroom_el, 'denominator')
        denominator.text = '1'

    if headroom:
        footroom_el = _subelement(container, 'headroom')
        numerator = _subelement(footroom_el, 'numerator')
        numerator.text = headroom
        denominator = _subelement(footroom_el, 'denominator')
        denominator.text = '1'

    return container


def format_characteristics(child_elements=None):
    """Creates the MIX SpecialFormatCharacteristics element."""

    container = _element('SpecialFormatCharacteristics')

    if child_elements:
        for element in child_elements:
            container.append(element)

    return container


def jpeg200(codec=None, codec_version=None, codestream_profile=None,
            compliance_class=None, tile_width=None, tile_height=None,
            quality_layers=None, resolution_levels=None):
    """Creates the MIX JPEG2000 element."""

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
            tile_width_el.text = tile_width
        if tile_height:
            tile_height_el = _subelement(tiles_container, 'tileHeight')
            tile_height_el.text = tile_height

    if tiles_container or quality_layers or resolution_levels:
        encoding_options = _subelement(container, 'EncodingOptions')
        if tiles_container:
            encoding_options.append(tiles_container)
        if quality_layers:
            quality_layers_el = _subelement(
                encoding_options, 'qualityLayers')
            quality_layers_el.text = quality_layers
        if resolution_levels:
            resolution_levels_el = _subelement(
                encoding_options, 'resolutionLevels')
            resolution_levels_el.text = resolution_levels

    return container


def mrsid(zoom_levels=None):
    """Creates the MIX MrSID element."""

    container = _element('MrSID')

    if zoom_levels:
        zoom_levels_el = _subelement(container, 'zoomLevels')
        zoom_levels_el.text = zoom_levels

    return container


def djvu(djvu_format=None):
    """Creates the MIX Djvu element."""

    container = _element('Djvu')

    if djvu_format:
        djvu_format_el = _subelement(container, 'djvuFormat')
        djvu_format_el.text = djvu_format

    return container
