"""Test nisomix features."""
import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.mix import _element
from nisomix.image_information import (image_information,
                                       image_characteristics,
                                       photometric_interpretation,
                                       color_profile, ycbcr,
                                       ref_black_white, component)


def test_image_information():
    """Test that the element BasicImageInformation is
    created correctly.
    """

    img_characteristics = _element('BasicImageCharacteristics')
    format_characteristics = _element('SpecialFormatCharacteristics')
    mix = image_information(child_elements=[img_characteristics,
                                            format_characteristics])

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
    mix = image_characteristics(width='1', height='2',
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
    Test that the element PhotometricInterpretation is created correctly.
    """

    profile = _element('ColorProfile')
    mix = photometric_interpretation(color_space='foo',
                                     child_elements=[profile])

    xml_str = ('<mix:PhotometricInterpretation '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:colorSpace>foo</mix:colorSpace>'
               '<mix:ColorProfile/></mix:PhotometricInterpretation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_color_profile():
    """Test that the element ColorProfile is created correctly."""

    profile = color_profile(icc_name='foo', icc_version='1',
                            icc_uri='http://foo')

    xml_str = ('<mix:ColorProfile xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:IccProfile><mix:iccProfileName>foo</mix:iccProfileName>'
               '<mix:iccProfileVersion>1</mix:iccProfileVersion>'
               '<mix:iccProfileURI>http://foo</mix:iccProfileURI>'
               '</mix:IccProfile></mix:ColorProfile>')

    assert h.compare_trees(profile, ET.fromstring(xml_str))


def test_ycbcr():
    """Test that the element YCbCr is created correctly."""

    mix = ycbcr(subsample_horiz='1', subsample_vert='2',
                positioning='2', luma_red='1', luma_green='2', luma_blue='3')

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
    """Test that the element YCbCr is created correctly."""

    mix = component(c_photometric_interpretation='R', footroom='1',
                    headroom='2')

    xml_str = ('<mix:Component xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:componentPhotometricInterpretation>R'
               '</mix:componentPhotometricInterpretation>'
               '<mix:footroom><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:footroom>'
               '<mix:headroom><mix:numerator>2</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:headroom>'
               '</mix:Component>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
