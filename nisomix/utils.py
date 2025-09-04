"""Utility functions for nisomix."""
from __future__ import annotations


import lxml.etree as ET
from xml_helpers.utils import XSI_NS


MIX_NS = 'http://www.loc.gov/mix/v20'

NAMESPACES = {'mix': MIX_NS,
              'xsi': XSI_NS}


class RestrictedElementError(Exception):
    """Raised when the value of a restricted element is invalid."""

    def __str__(self):
        """List accepted values for the restricted element."""
        accepted_values = '", "'.join(self.args[2])
        return (f'The value "{self.args[0]}" is invalid for {self.args[1]}, '
                f'accepted values are: "{accepted_values}".')


def mix_root_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the mix root element in the correct
    sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}BasicDigitalObjectInformation",
            f"{{{MIX_NS}}}BasicImageInformation",
            f"{{{MIX_NS}}}ImageCaptureMetadata",
            f"{{{MIX_NS}}}ImageAssessmentMetadata",
            f"{{{MIX_NS}}}ChangeHistory",
            f"{{{MIX_NS}}}Extension"].index(elem.tag)


def basic_do_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the BasicDigitalObjectInformation parent
    element in the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}ObjectIdentifier",
            f"{{{MIX_NS}}}fileSize",
            f"{{{MIX_NS}}}FormatDesignation",
            f"{{{MIX_NS}}}FormatRegistry",
            f"{{{MIX_NS}}}byteOrder",
            f"{{{MIX_NS}}}Compression",
            f"{{{MIX_NS}}}Fixity"].index(elem.tag)


def image_information_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the BasicImageInformation parent element in
    the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}BasicImageCharacteristics",
            f"{{{MIX_NS}}}SpecialFormatCharacteristics"].index(elem.tag)


def photom_interpret_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the PhotometricInterpretation parent element
    in the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}colorSpace",
            f"{{{MIX_NS}}}ColorProfile",
            f"{{{MIX_NS}}}YCbCr",
            f"{{{MIX_NS}}}ReferenceBlackWhite"].index(elem.tag)


def image_capture_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ImageCaptureMetadataType parent element in
    the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}SourceInformation",
            f"{{{MIX_NS}}}GeneralCaptureInformation",
            f"{{{MIX_NS}}}ScannerCapture",
            f"{{{MIX_NS}}}DigitalCameraCapture",
            f"{{{MIX_NS}}}orientation",
            f"{{{MIX_NS}}}methodology"].index(elem.tag)


def source_information_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the SourceInformation parent element in the
    correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}sourceType",
            f"{{{MIX_NS}}}SourceID",
            f"{{{MIX_NS}}}SourceSize"].index(elem.tag)


def scanner_capture_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ScannerCapture parent element in the
    correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}scannerManufacturer",
            f"{{{MIX_NS}}}ScannerModel",
            f"{{{MIX_NS}}}MaximumOpticalResolution",
            f"{{{MIX_NS}}}scannerSensor",
            f"{{{MIX_NS}}}ScanningSystemSoftware"].index(elem.tag)


def camera_capture_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the DigitalCameraCapture parent element in
    the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}digitalCameraManufacturer",
            f"{{{MIX_NS}}}DigitalCameraModel",
            f"{{{MIX_NS}}}cameraSensor",
            f"{{{MIX_NS}}}CameraCaptureSettings"].index(elem.tag)


def camera_capture_settings_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the CameraCaptureSettings parent element in
    the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}ImageData",
            f"{{{MIX_NS}}}GPSData"].index(elem.tag)


def image_data_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ImageData parent element in the correct
    sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}fNumber",
            f"{{{MIX_NS}}}exposureTime",
            f"{{{MIX_NS}}}exposureProgram",
            f"{{{MIX_NS}}}spectralSensitivity",
            f"{{{MIX_NS}}}isoSpeedRatings",
            f"{{{MIX_NS}}}oECF",
            f"{{{MIX_NS}}}exifVersion",
            f"{{{MIX_NS}}}shutterSpeedValue",
            f"{{{MIX_NS}}}apertureValue",
            f"{{{MIX_NS}}}brightnessValue",
            f"{{{MIX_NS}}}exposureBiasValue",
            f"{{{MIX_NS}}}maxApertureValue",
            f"{{{MIX_NS}}}SubjectDistance",
            f"{{{MIX_NS}}}meteringMode",
            f"{{{MIX_NS}}}lightSource",
            f"{{{MIX_NS}}}flash",
            f"{{{MIX_NS}}}focalLength",
            f"{{{MIX_NS}}}flashEnergy",
            f"{{{MIX_NS}}}backLight",
            f"{{{MIX_NS}}}exposureIndex",
            f"{{{MIX_NS}}}sensingMethod",
            f"{{{MIX_NS}}}cfaPattern",
            f"{{{MIX_NS}}}autoFocus",
            f"{{{MIX_NS}}}PrintAspectRatio"].index(elem.tag)


def gps_data_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the GPSData parent element in the correct
    sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}gpsVersionID",
            f"{{{MIX_NS}}}gpsLatitudeRef",
            f"{{{MIX_NS}}}GPSLatitude",
            f"{{{MIX_NS}}}gpsLongitudeRef",
            f"{{{MIX_NS}}}GPSLongitude",
            f"{{{MIX_NS}}}gpsAltitudeRef",
            f"{{{MIX_NS}}}gpsAltitude",
            f"{{{MIX_NS}}}gpsTimeStamp",
            f"{{{MIX_NS}}}gpsSatellites",
            f"{{{MIX_NS}}}gpsStatus",
            f"{{{MIX_NS}}}gpsMeasureMode",
            f"{{{MIX_NS}}}gpsDOP",
            f"{{{MIX_NS}}}gpsSpeedRef",
            f"{{{MIX_NS}}}gpsSpeed",
            f"{{{MIX_NS}}}gpsTrackRef",
            f"{{{MIX_NS}}}gpsTrack",
            f"{{{MIX_NS}}}gpsImgDirectionRef",
            f"{{{MIX_NS}}}gpsImgDirection",
            f"{{{MIX_NS}}}gpsMapDatum",
            f"{{{MIX_NS}}}gpsDestLatitudeRef",
            f"{{{MIX_NS}}}GPSDestLatitude",
            f"{{{MIX_NS}}}gpsDestLongitudeRef",
            f"{{{MIX_NS}}}GPSDestLongitude",
            f"{{{MIX_NS}}}gpsDestBearingRef",
            f"{{{MIX_NS}}}gpsDestBearing",
            f"{{{MIX_NS}}}gpsDestDistanceRef",
            f"{{{MIX_NS}}}gpsDestDistance",
            f"{{{MIX_NS}}}gpsProcessingMethod",
            f"{{{MIX_NS}}}gpsAreaInformation",
            f"{{{MIX_NS}}}gpsDateStamp",
            f"{{{MIX_NS}}}gpsDifferential"].index(elem.tag)


def assessment_metadata_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ImageAssessmentMetadata parent element in
    the correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}SpatialMetrics",
            f"{{{MIX_NS}}}ImageColorEncoding",
            f"{{{MIX_NS}}}TargetData"].index(elem.tag)


def color_encoding_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ImageColorEncoding parent element in the
    correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}BitsPerSample",
            f"{{{MIX_NS}}}samplesPerPixel",
            f"{{{MIX_NS}}}extraSamples",
            f"{{{MIX_NS}}}Colormap",
            f"{{{MIX_NS}}}GrayResponse",
            f"{{{MIX_NS}}}WhitePoint",
            f"{{{MIX_NS}}}PrimaryChromaticities"].index(elem.tag)


def target_data_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the TargetData parent element in the correct
    sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}targetType",
            f"{{{MIX_NS}}}TargetID",
            f"{{{MIX_NS}}}externalTarget",
            f"{{{MIX_NS}}}performanceData"].index(elem.tag)


def change_history_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ChangeHistory parent element in the
    correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}ImageProcessing",
            f"{{{MIX_NS}}}PreviousImageMetadata"].index(elem.tag)


def image_processing_order(elem: ET._Element) -> int:
    """
    Sorts the elements in the ImageProcessing parent element in the
    correct sequence.

    :param elem: XML Element
    :returns: Index of the element's tag in the expected order
    """
    return [f"{{{MIX_NS}}}dateTimeProcessed",
            f"{{{MIX_NS}}}sourceData",
            f"{{{MIX_NS}}}processingAgency",
            f"{{{MIX_NS}}}processingRationale",
            f"{{{MIX_NS}}}ProcessingSoftware",
            f"{{{MIX_NS}}}processingActions"].index(elem.tag)
