import pytest
from nisomix.mix import (MIX_NS, mix_ns, mix_mix,
                         mix_Compression,
                         mix_BasicDigitalObjectInformation,
                         mix_BasicImageInformation,
                         mix_Component,
                         mix_ImageAssessmentMetadata,
                         mix_PrimaryChromaticities,
                         mix_ReferenceBlackWhite,
                         mix_TargetID,
                         mix_WhitePoint)

NAMESPACES = {'mix': MIX_NS}


@pytest.mark.parametrize(('tag', 'prefix'), [
    ('first', None),
    ('second', 'myPrefix'),
])
def test_mix_ns(tag, prefix):
    new_ns = mix_ns(tag, prefix)
    if prefix:
        assert prefix in new_ns
        tag = tag[0].upper() + tag[1:]
    assert tag in new_ns


def _assert_mix_obj(mix_obj):
    assert mix_obj.xpath(
        "/mix:mix/mix:BasicDigitalObjectInformation/mix:byteOrder",
        namespaces=NAMESPACES)[0].text == 'big endian'
    assert mix_obj.xpath(
        ("/mix:mix/mix:BasicDigitalObjectInformation/mix:Compression/"
         "mix:compressionScheme"),
        namespaces=NAMESPACES)[0].text == 'JPEG 2000 Lossless'
    assert mix_obj.xpath(
        ("/mix:mix/mix:BasicDigitalObjectInformation/mix:Compression/"
         "mix:compressionRatio"),
        namespaces=NAMESPACES)[0].text == '10'


def test_mix_ok():
    mix1 = mix_mix()
    compression = mix_Compression(
        compressionScheme='JPEG 2000 Lossless',
        compressionRatio='10'
    )

    basicDigitalObjectInformation = mix_BasicDigitalObjectInformation(
        byteOrder='big endian',
        Compression_elements=[compression]
    )

    basicImageInformation = mix_BasicImageInformation(
        imageWidth='1024',
        imageHeight='768', colorSpace='ICCBased', iccProfileName='Adobe RGB',
        iccProfileVersion='1998',
        iccProfileURI='http://www.adobe.com/digitalimag/adobergb.html',
        qualityLayers='12', resolutionLevels='6'
    )

    imageAssessmentMetadata = mix_ImageAssessmentMetadata(
        bitsPerSampleValue_elements=['16, 16, 16'],
        bitsPerSampleUnit='integer', samplesPerPixel='4',
        extraSamples_elements=['unspecified data'],
        colormapReference='http://foo.bar'
    )

    mix1.append(basicDigitalObjectInformation)
    mix1.append(basicImageInformation)
    mix1.append(imageAssessmentMetadata)
    _assert_mix_obj(mix1)


def test_mix_mix():
    compression = mix_Compression(
        compressionScheme='JPEG 2000 Lossless',
        compressionRatio='10'
    )

    compression2 = mix_Compression(
        compressionScheme='enumerated in local list',
        compressionSchemeLocalList='file:///tmp/tmpschemelist',
        compressionSchemeLocalValue='JPEG 2000 Lossless',
        compressionRatio='10'
    )
    basicDigitalObjectInformation = mix_BasicDigitalObjectInformation(
        byteOrder='big endian',
        Compression_elements=[compression, compression2]
    )

    basicImageInformation = mix_BasicImageInformation(
        imageWidth='1024',
        imageHeight='768', colorSpace='ICCBased', iccProfileName='Adobe RGB',
        iccProfileVersion='1998',
        iccProfileURI='http://www.adobe.com/digitalimag/adobergb.html',
        localProfileName='Adobe RGB',
        localProfileURL='http://www.adobe.com/digitalimag/adobergb.html',
        embeddedProfile='QWRvYmUgUkdC',  # Base64 encoded.
        yCbCrSubsampleHoriz='1', yCbCrSubsampleVert='2', yCbCrPositioning='1',
        lumaRed='1', lumaGreen='1', lumaBlue='1',
        ReferenceBlackWhite_elements=[
            mix_ReferenceBlackWhite([
                mix_Component(
                    componentPhotometricInterpretation='R',
                    headroom='1',
                    footroom='1'
                )
            ])
        ],
        codec='OpenJPEG', codecVersion='2.3.0', codestreamProfile='P0',
        complianceClass='C0',
        tileWidth='1', tileHeight='1',
        zoomLevels='1',
        djvuFormat='bundled',
        qualityLayers='12', resolutionLevels='6'
    )

    imageAssessmentMetadata = mix_ImageAssessmentMetadata(
        bitsPerSampleValue_elements=['16, 16, 16'],
        bitsPerSampleUnit='integer', samplesPerPixel='4',
        extraSamples_elements=[
            'unspecified data'],
        colormapReference='http://foo.bar',
        samplingFrequencyPlane='camera/scanner focal plane',
        samplingFrequencyUnit='no absolute unit of measurement',
        xSamplingFrequency='1',
        ySamplingFrequency='1',
        embeddedColormap='d2hpdGU=',  # Base64 encoded.
        grayResponseCurve_elements=['64'],
        grayResponseUnit='3',
        WhitePoint_elements=[
            mix_WhitePoint(whitePointXValue='1', whitePointYValue='1')
        ],
        PrimaryChromaticities_elements=[
            mix_PrimaryChromaticities(
                primaryChromaticitiesRedX='1',
                primaryChromaticitiesRedY='1',
                primaryChromaticitiesGreenX='1',
                primaryChromaticitiesGreenY='1',
                primaryChromaticitiesBlueX='1',
                primaryChromaticitiesBlueY='1'
            )
        ],
        targetType_elements=['0'],
        TargetID_elements=[
            mix_TargetID(
                targetManufacturer='Foobar Inc',
                targetName='Foo',
                targetNo='Version 1',
                targetMedia='Ektachrome Transparency'
            )
        ],
        externalTarget_elements=['foobar.jpg'],
        performanceData_elements=['foobar.txt']

    )

    mix2 = mix_mix(BasicDigitalObjectInformation=basicDigitalObjectInformation,
                   BasicImageInformation=basicImageInformation,
                   ImageAssessmentMetadata=imageAssessmentMetadata)

    _assert_mix_obj(mix2)
