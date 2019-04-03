# encoding=utf8
"""Utility functions and global variables."""

from xml_helpers.utils import XSI_NS


MIX_NS = 'http://www.loc.gov/mix/v20'

NAMESPACES = {'mix': MIX_NS,
              'xsi': XSI_NS}

BYTE_ORDER_TYPES = ['big endian', 'little endian']

DIGEST_ALGORITHMS = ['Adler-32', 'CRC32', 'HAVAL', 'MD5', 'MNP', 'SHA-1',
                     'SHA-256', 'SHA-384', 'SHA-512', 'TIGER', 'WHIRLPOOL',
                     'unknown']

YCBCR_SUBSAMPLE_TYPES = ['1', '2', '4']

YCBCR_POSITIONING_TYPES = ['1', '2']

COMPONENT_INTERPRETATION_TYPES = ['R', 'G', 'B', 'Y', 'Cb', 'Cr']

ORIENTATION_TYPES = [
    'normal*', 'normal, image flipped', 'normal, rotated 180°',
    'normal, image flipped, rotated 180°',
    'normal, image flipped, rotated cw 90°',
    'normal, rotated ccw 90°',
    'normal, image flipped, rotated ccw 90°',
    'normal, rotated cw 90°', 'unknown']

DJVU_FORMATS = ['indirect', 'bundled']

DIMENSION_UNITS = ['in.', 'mm']

OPTICAL_RESOLUTION_UNITS = ['no absolute unit', 'in.', 'cm']

CAPTURE_DEVICE_TYPES = ['transmission scanner', 'reflection print scanner',
                        'digital still camera', 'still from video']

SCANNER_SENSOR_TYPES = [
    'undefined', 'MonochromeLinear', 'ColorTriLinear',
    'ColorSequentialLinear', 'MonochromeArea', 'OneChipColourArea',
    'TwoChipColorArea', 'ThreeChipColorArea', 'ColorSequentialArea']

CAMERA_SENSOR_TYPES = [
    'undefined', 'MonochromeArea', 'OneChipColorArea',
    'TwoChipColorArea', 'ThreeChipColorArea', 'MonochromeLinear',
    'ColorTriLinear', 'ColorSequentialLinear']

EXPOSURE_PROGRAM_TYPES = [
    'Not defined', 'Manual', 'Normal program', 'Aperture priority',
    'Shutter priority', 'Creative program (biased toward depth of field)',
    'Action program (biased toward fast shutter speed)',
    'Portrait mode (for closeup photos with the background out of focus)',
    'Landscape mode (for landscape photos with the background in focus)']

EXIF_VERSION_TYPES = ['0220', '0221']

METERING_MODE_TYPES = ['Average', 'Center weighted average', 'Spot',
                       'Multispot', 'Pattern', 'Partial']

SAMPLING_FREQUENCY_PLANES = ['camera/scanner focal plane', 'object plane',
                             'source object plane']

SAMPLING_FREQUENCY_UNITS = ['no absolute unit of measurement', 'in.', 'cm']

BITS_PER_SAMPLE_UNITS = ['integer', 'floating point']

EXTRA_SAMPLES_TYPES = ['unspecified data',
                       'associated alpha data (with pre-multiplied color)',
                       'unassociated alpha data', 'range or depth data']

GRAY_RESPONSE_UNITS = ['Number represents tenths of a unit',
                       'Number represents hundredths of a unit',
                       'Number represents thousandths of a unit',
                       'Number represents ten-thousandths of a unit',
                       'Number represents hundred-thousandths of a unit']

TARGET_TYPES = ['external', 'internal']


class RestrictedElementError(Exception):
    """Raised when the value of a restricted element is invalid."""
    pass


def mix_root_order(elem):
    """Sorts the elements in the mix root element in the correct sequence."""
    return ['{%s}BasicDigitalObjectInformation' % MIX_NS,
            '{%s}BasicImageInformation' % MIX_NS,
            '{%s}ImageCaptureMetadata' % MIX_NS,
            '{%s}ImageAssessmentMetadata' % MIX_NS,
            '{%s}ChangeHistory' % MIX_NS,
            '{%s}Extension' % MIX_NS].index(elem.tag)


def basic_do_order(elem):
    """
    Sorts the elements in the BasicDigitalObjectInformation parent
    element in the correct sequence.
    """
    return ['{%s}ObjectIdentifier' % MIX_NS,
            '{%s}fileSize' % MIX_NS,
            '{%s}FormatDesignation' % MIX_NS,
            '{%s}FormatRegistry' % MIX_NS,
            '{%s}byteOrder' % MIX_NS,
            '{%s}Compression' % MIX_NS,
            '{%s}Fixity' % MIX_NS].index(elem.tag)


def image_information_order(elem):
    """
    Sorts the elements in the BasicImageInformation parent
    element in the correct sequence.
    """
    return ['{%s}BasicImageCharacteristics' % MIX_NS,
            '{%s}SpecialFormatCharacteristics' % MIX_NS].index(elem.tag)


def photom_interpret_order(elem):
    """
    Sorts the elements in the PhotometricInterpretation parent
    element in the correct sequence.
    """
    return ['{%s}colorSpace' % MIX_NS,
            '{%s}ColorProfile' % MIX_NS,
            '{%s}YCbCr' % MIX_NS,
            '{%s}ReferenceBlackWhite' % MIX_NS].index(elem.tag)


def image_capture_order(elem):
    """
    Sorts the elements in the ImageCaptureMetadataType parent
    element in the correct sequence.
    """
    return ['{%s}SourceInformation' % MIX_NS,
            '{%s}GeneralCaptureInformation' % MIX_NS,
            '{%s}ScannerCapture' % MIX_NS,
            '{%s}DigitalCameraCapture' % MIX_NS,
            '{%s}orientation' % MIX_NS,
            '{%s}methodology' % MIX_NS].index(elem.tag)


def scanner_capture_order(elem):
    """
    Sorts the elements in the ScannerCapture parent
    element in the correct sequence.
    """
    return ['{%s}scannerManufacturer' % MIX_NS,
            '{%s}ScannerModel' % MIX_NS,
            '{%s}MaximumOpticalResolution' % MIX_NS,
            '{%s}scannerSensor' % MIX_NS,
            '{%s}ScanningSystemSoftware' % MIX_NS].index(elem.tag)


def camera_capture_order(elem):
    """
    Sorts the elements in the DigitalCameraCapture parent
    element in the correct sequence.
    """
    return ['{%s}digitalCameraManufacturer' % MIX_NS,
            '{%s}DigitalCameraModel' % MIX_NS,
            '{%s}cameraSensor' % MIX_NS,
            '{%s}CameraCaptureSettings' % MIX_NS].index(elem.tag)


def camera_capture_settings_order(elem):
    """
    Sorts the elements in the CameraCaptureSettings parent
    element in the correct sequence.
    """
    return ['{%s}ImageData' % MIX_NS,
            '{%s}GPSData' % MIX_NS].index(elem.tag)


def image_data_order(elem):
    """
    Sorts the elements in the ImageData parent
    element in the correct sequence.
    """
    return ['{%s}fNumber' % MIX_NS,
            '{%s}exposureTime' % MIX_NS,
            '{%s}exposureProgram' % MIX_NS,
            '{%s}spectralSensitivity' % MIX_NS,
            '{%s}isoSpeedRatings' % MIX_NS,
            '{%s}oECF' % MIX_NS,
            '{%s}exifVersion' % MIX_NS,
            '{%s}shutterSpeedValue' % MIX_NS,
            '{%s}apertureValue' % MIX_NS,
            '{%s}brightnessValue' % MIX_NS,
            '{%s}exposureBiasValue' % MIX_NS,
            '{%s}maxApertureValue' % MIX_NS,
            '{%s}SubjectDistance' % MIX_NS,
            '{%s}meteringMode' % MIX_NS,
            '{%s}lightSource' % MIX_NS,
            '{%s}flash' % MIX_NS,
            '{%s}focalLength' % MIX_NS,
            '{%s}flashEnergy' % MIX_NS,
            '{%s}backLight' % MIX_NS,
            '{%s}exposureIndex' % MIX_NS,
            '{%s}sensingMethod' % MIX_NS,
            '{%s}cfaPattern' % MIX_NS,
            '{%s}autoFocus' % MIX_NS,
            '{%s}PrintAspectRatio' % MIX_NS].index(elem.tag)


def gps_data_order(elem):
    """
    Sorts the elements in the GPSData parent
    element in the correct sequence.
    """
    return ['{%s}gpsVersionID' % MIX_NS,
            '{%s}gpsLatitudeRef' % MIX_NS,
            '{%s}GPSLatitude' % MIX_NS,
            '{%s}gpsLongitudeRef' % MIX_NS,
            '{%s}GPSLongitude' % MIX_NS,
            '{%s}gpsAltitudeRef' % MIX_NS,
            '{%s}gpsAltitude' % MIX_NS,
            '{%s}gpsTimeStamp' % MIX_NS,
            '{%s}gpsSatellites' % MIX_NS,
            '{%s}gpsStatus' % MIX_NS,
            '{%s}gpsMeasureMode' % MIX_NS,
            '{%s}gpsDOP' % MIX_NS,
            '{%s}gpsSpeedRef' % MIX_NS,
            '{%s}gpsSpeed' % MIX_NS,
            '{%s}gpsTrackRef' % MIX_NS,
            '{%s}gpsTrack' % MIX_NS,
            '{%s}gpsImgDirectionRef' % MIX_NS,
            '{%s}gpsImgDirection' % MIX_NS,
            '{%s}gpsMapDatum' % MIX_NS,
            '{%s}gpsDestLatitudeRef' % MIX_NS,
            '{%s}GPSDestLatitude' % MIX_NS,
            '{%s}gpsDestLongitudeRef' % MIX_NS,
            '{%s}GPSDestLongitude' % MIX_NS,
            '{%s}gpsDestBearingRef' % MIX_NS,
            '{%s}gpsDestBearing' % MIX_NS,
            '{%s}gpsDestDistanceRef' % MIX_NS,
            '{%s}gpsDestDistance' % MIX_NS,
            '{%s}gpsProcessingMethod' % MIX_NS,
            '{%s}gpsAreaInformation' % MIX_NS,
            '{%s}gpsDateStamp' % MIX_NS,
            '{%s}gpsDifferential' % MIX_NS].index(elem.tag)


def assessment_metadata_order(elem):
    """
    Sorts the elements in the ImageAssessmentMetadata
    parent element in the correct sequence.
    """
    return ['{%s}SpatialMetrics' % MIX_NS,
            '{%s}ImageColorEncoding' % MIX_NS,
            '{%s}TargetData' % MIX_NS].index(elem.tag)


def color_encoding_order(elem):
    """
    Sorts the elements in the ImageColorEncoding
    parent element in the correct sequence.
    """
    return ['{%s}BitsPerSample' % MIX_NS,
            '{%s}samplesPerPixel' % MIX_NS,
            '{%s}extraSamples' % MIX_NS,
            '{%s}Colormap' % MIX_NS,
            '{%s}GrayResponse' % MIX_NS,
            '{%s}WhitePoint' % MIX_NS,
            '{%s}PrimaryChromaticities' % MIX_NS].index(elem.tag)


def target_data_order(elem):
    """
    Sorts the elements in the TargetData
    parent element in the correct sequence.
    """
    return ['{%s}targetType' % MIX_NS,
            '{%s}TargetID' % MIX_NS,
            '{%s}externalTarget' % MIX_NS,
            '{%s}performanceData' % MIX_NS].index(elem.tag)
