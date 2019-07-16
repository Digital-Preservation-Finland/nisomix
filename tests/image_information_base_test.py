"""Test nisomix.image_information_base module functions."""
from __future__ import unicode_literals

import pytest

import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.base import _element
from nisomix.image_information_base import (color_profile, component, djvu,
                                            format_characteristics,
                                            image_characteristics,
                                            image_information, jpeg2000, mrsid,
                                            photometric_interpretation,
                                            ref_black_white, ycbcr)
from nisomix.utils import RestrictedElementError


def test_image_information():
    """
    Tests that the element BasicImageInformation is created correctly
    and that the subelements are sorted properly.
    """

    img_characteristics = _element('BasicImageCharacteristics')
    f_characteristics = _element('SpecialFormatCharacteristics')
    mix = image_information(child_elements=[f_characteristics,
                                            img_characteristics])

    xml_str = ('<mix:BasicImageInformation xmlns:mix='
               '"http://www.loc.gov/mix/v20">'
               '<mix:BasicImageCharacteristics/>'
               '<mix:SpecialFormatCharacteristics/>'
               '</mix:BasicImageInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_characteristics():
    """
    Test that the element BasicImageCharacteristics is created
    correctly.
    """

    interpretation = _element('PhotometricInterpretation')
    mix = image_characteristics(width=1, height=2,
                                child_elements=[interpretation])

    xml_str = ('<mix:BasicImageCharacteristics '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:imageWidth>1</mix:imageWidth>'
               '<mix:imageHeight>2</mix:imageHeight>'
               '<mix:PhotometricInterpretation/>'
               '</mix:BasicImageCharacteristics>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_photometric_interpretation():
    """
    Test that the element PhotometricInterpretation is created
    correctly.
    """

    profile = _element('ColorProfile')
    ycc = _element('YCbCr')
    ref_bw = _element('ReferenceBlackWhite')
    mix = photometric_interpretation(color_space='foo',
                                     child_elements=[ycc, ref_bw, profile])

    xml_str = ('<mix:PhotometricInterpretation '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:colorSpace>foo</mix:colorSpace>'
               '<mix:ColorProfile/><mix:YCbCr/><mix:ReferenceBlackWhite/>'
               '</mix:PhotometricInterpretation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_color_profile():
    """Test that the element ColorProfile is created correctly."""

    profile = color_profile(icc_name='foo', icc_version='1',
                            icc_uri='http://foo', local_name='local',
                            local_url='http://local', embedded_profile='2')

    xml_str = ('<mix:ColorProfile xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:IccProfile><mix:iccProfileName>foo</mix:iccProfileName>'
               '<mix:iccProfileVersion>1</mix:iccProfileVersion>'
               '<mix:iccProfileURI>http://foo</mix:iccProfileURI>'
               '</mix:IccProfile><mix:LocalProfile><mix:localProfileName>'
               'local</mix:localProfileName><mix:localProfileURL>http://local'
               '</mix:localProfileURL></mix:LocalProfile><mix:embeddedProfile>'
               '2</mix:embeddedProfile></mix:ColorProfile>')

    assert h.compare_trees(profile, ET.fromstring(xml_str))


def test_ycbcr():
    """Test that the element YCbCr is created correctly."""

    mix = ycbcr(subsample_horiz='1', subsample_vert='2',
                positioning='2', luma_red=1, luma_green=2, luma_blue=3)

    xml_str = ('<mix:YCbCr xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:YCbCrSubSampling>'
               '<mix:yCbCrSubsampleHoriz>1</mix:yCbCrSubsampleHoriz>'
               '<mix:yCbCrSubsampleVert>2</mix:yCbCrSubsampleVert>'
               '</mix:YCbCrSubSampling>'
               '<mix:yCbCrPositioning>2</mix:yCbCrPositioning>'
               '<mix:YCbCrCoefficients><mix:lumaRed>'
               '<mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:lumaRed>'
               '<mix:lumaGreen><mix:numerator>2</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:lumaGreen>'
               '<mix:lumaBlue><mix:numerator>3</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:lumaBlue>'
               '</mix:YCbCrCoefficients></mix:YCbCr>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


@pytest.mark.parametrize(('horiz', 'vert', 'positioning'), [
    ('foo', '1', '1'),
    ('1', 'foo', '1'),
    ('1', '1', 'foo')])
def test_ycbcr_error(horiz, vert, positioning):
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        ycbcr(subsample_horiz=horiz, subsample_vert=vert,
              positioning=positioning)


def test_ref_black_white():
    """Test that the element ReferenceBlackWhite is created correctly."""

    comp1 = _element('Component')
    comp2 = _element('Component')
    mix = ref_black_white(child_elements=[comp1, comp2])

    xml_str = ('<mix:ReferenceBlackWhite '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:Component/><mix:Component/>'
               '</mix:ReferenceBlackWhite>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_component():
    """Test that the element Component is created correctly."""

    mix = component(c_photometric_interpretation='R', footroom=1,
                    headroom=2)

    xml_str = ('<mix:Component xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:componentPhotometricInterpretation>R'
               '</mix:componentPhotometricInterpretation>'
               '<mix:footroom><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:footroom>'
               '<mix:headroom><mix:numerator>2</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:headroom>'
               '</mix:Component>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_component_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        component(c_photometric_interpretation='foo')


def test_format_characteristics():
    """
    Test that the element SpecialFormatCharacteristics is created
    correctly.
    """
    jp2000 = _element('JPEG2000')
    mix = format_characteristics(child_elements=[jp2000])

    xml_str = ('<mix:SpecialFormatCharacteristics '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:JPEG2000/>'
               '</mix:SpecialFormatCharacteristics>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_jpeg2000():
    """Test that the element JPEG2000 is created correctly."""
    mix = jpeg2000(codec='jp2', codec_version='1.0', codestream_profile='P1',
                   compliance_class='C0', tile_width=1, tile_height=2,
                   quality_layers=3, resolution_levels=4)

    xml_str = ('<mix:JPEG2000 xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:CodecCompliance><mix:codec>jp2</mix:codec>'
               '<mix:codecVersion>1.0</mix:codecVersion>'
               '<mix:codestreamProfile>P1</mix:codestreamProfile>'
               '<mix:complianceClass>C0</mix:complianceClass>'
               '</mix:CodecCompliance><mix:EncodingOptions><mix:Tiles>'
               '<mix:tileWidth>1</mix:tileWidth>'
               '<mix:tileHeight>2</mix:tileHeight></mix:Tiles>'
               '<mix:qualityLayers>3</mix:qualityLayers>'
               '<mix:resolutionLevels>4</mix:resolutionLevels>'
               '</mix:EncodingOptions></mix:JPEG2000>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_mrsid():
    """Test that the element MrSID is created correctly."""
    mix = mrsid(zoom_levels=3)

    xml_str = ('<mix:MrSID xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:zoomLevels>3</mix:zoomLevels>'
               '</mix:MrSID>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_djvu():
    """
    Test that the element Djvu is created correctly. Also test that
    invalid djvu_format value raises an error.
    """
    mix = djvu(djvu_format='bundled')

    xml_str = ('<mix:Djvu xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:djvuFormat>bundled</mix:djvuFormat>'
               '</mix:Djvu>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    with pytest.raises(RestrictedElementError):
        djvu(djvu_format='foo')
