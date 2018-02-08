import nisomix.mix as miks
import pytest
import os

NAMESPACES = {'mix': miks.MIX_NS}

def test_mix_ok():

    mix = miks.mix_mix()
    compression = miks.mix_Compression(compressionScheme='JPEG 2000 Lossless',
                                       compressionRatio='10')

    basicDigitalObjectInformation = miks.mix_BasicDigitalObjectInformation(byteOrder='big endian',
                                                                           Compression_elements=[compression])

    basicImageInformation = miks.mix_BasicImageInformation(imageWidth='1024',
                                                           imageHeight='768', colorSpace='ICCBased', iccProfileName='Adobe RGB',
                                                           iccProfileVersion='1998',
                                                           iccProfileURI='http://www.adobe.com/digitalimag/adobergb.html',
                                                           qualityLayers='12', resolutionLevels='6')

    imageAssessmentMetadata = miks.mix_ImageAssessmentMetadata(bitsPerSampleValue_elements=['16, 16, 16'],
                                                               bitsPerSampleUnit='integer', samplesPerPixel='4',
                                                               extraSamples_elements=[
        'unspecified data'],
        colormapReference='http://foo.bar')

    mix.append(basicDigitalObjectInformation)
    mix.append(basicImageInformation)
    mix.append(imageAssessmentMetadata)

    assert mix.xpath("/mix:mix/mix:BasicDigitalObjectInformation/mix:byteOrder",
                      namespaces=NAMESPACES)[0].text == 'big endian'
    assert mix.xpath("/mix:mix/mix:BasicDigitalObjectInformation/mix:Compression/mix:compressionScheme",
                      namespaces=NAMESPACES)[0].text == 'JPEG 2000 Lossless'
    assert mix.xpath("/mix:mix/mix:BasicDigitalObjectInformation/mix:Compression/mix:compressionRatio",
                      namespaces=NAMESPACES)[0].text == '10'
