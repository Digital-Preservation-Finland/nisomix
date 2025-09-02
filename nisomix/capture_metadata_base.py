"""
Functions for reading and generating MIX Image Capture Metadata as
xml.etree.ElementTree data structures.

References:

    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images
                            (ANSI/NISO Z39.87-2006 (R2017))
                            Chapter 8: Image Capture Metadata
    * ElementTree
    https://docs.python.org/3.9/library/xml.etree.elementtree.html

"""
from __future__ import annotations

import lxml.etree as ET

from nisomix.base import (
    _element,
    _ensure_list,
    _rationaltype_element,
    _subelement,
    mix_ns,
)
from nisomix.constants import (
    CAMERA_SENSOR_TYPES,
    CAPTURE_DEVICE_TYPES,
    DIMENSION_UNITS,
    GPS_DATA_CONTENTS,
    IMAGE_DATA_CONTENTS,
    OPTICAL_RESOLUTION_UNITS,
    ORIENTATION_TYPES,
    SCANNER_SENSOR_TYPES,
)
from nisomix.utils import (
    NAMESPACES,
    RestrictedElementError,
    camera_capture_order,
    camera_capture_settings_order,
    gps_data_order,
    image_capture_order,
    image_data_order,
    scanner_capture_order,
    source_information_order,
)

__all__ = [
    'camera_capture_settings',
    'capture_information',
    'device_capture',
    'device_model',
    'gps_data',
    'image_capture_metadata',
    'image_data',
    'max_optical_resolution',
    'parse_datetime_created',
    'scanning_software',
    'source_id',
    'source_information',
    'source_size',
]


def image_capture_metadata(
    orientation: str | None = None,
    methodology: str | None = None,
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX ImageCaptureMetadata element.

    :param orientation: The image orientation as a string
    :param methodology: The digitization methodology as a string
    :param child_elements: Child elements as a list

    :returns:
    The following sorted ElementTree structure::

        <mix:ImageCaptureMetadata>
            {{ Child elements }}
            <mix:orientation>unknown</mix:orientation>
            <mix:methodology>unknown</mix:methodology>
        </mix:ImageCaptureMetadata>

    """
    if child_elements is None:
        child_elements = []

    container = _element('ImageCaptureMetadata')

    if orientation:
        if orientation in ORIENTATION_TYPES:
            orientation_el = _element('orientation')
            orientation_el.text = orientation
            child_elements.append(orientation_el)
        else:
            raise RestrictedElementError(
                orientation, 'orientation', ORIENTATION_TYPES)
    if methodology:
        methodology_el = _element('methodology')
        methodology_el.text = methodology
        child_elements.append(methodology_el)

    child_elements.sort(key=image_capture_order)

    for element in child_elements:
        container.append(element)

    return container


def source_information(
    source_type: str | None = None,
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX SourceInformation element.

    :param source_type: The source type as a string
    :param child_elements: Child elements as a list

    :returns:
    The following sorted ElementTree structure::

        <mix:SourceInformation>
            <mix:sourceType>foo</mix:sourceType>
            <mix:SourceID/>
            <mix:SourceSize/>
        </mix:SourceInformation>

    """
    container = _element('SourceInformation')

    if child_elements is None:
        child_elements = []

    if source_type:
        source_type_el = _element('sourceType')
        source_type_el.text = source_type
        child_elements.append(source_type_el)

    child_elements.sort(key=source_information_order)
    for element in child_elements:
        container.append(element)

    return container


def source_id(
    source_idtype: str | None = None, source_idvalue: str | None = None
) -> ET._Element:
    """
    Returns the MIX SourceID element.

    :param source_idtype: The source ID type as a string
    :param source_idvalue: The source ID value as a string

    :returns:
    The following sorted ElementTree structure::

        <mix:SourceID>
          <mix:sourceIDType>local</mix:sourceIDType>
          <mix:sourceIDValue>foo</mix:sourceIDValue>
        </mix:SourceID>

    """
    container = _element('SourceID')

    if source_idtype:
        source_idtype_el = _subelement(container, 'sourceIDType')
        source_idtype_el.text = source_idtype

    if source_idvalue:
        source_idvalue_el = _subelement(container, 'sourceIDValue')
        source_idvalue_el.text = source_idvalue

    return container


# pylint: disable=too-many-arguments, too-many-locals, too-many-branches
# too-many-arguments: The element contains a lot of subelements
# too-many-locals: The arguments are many, hence a lot of local variables
def source_size(
    x_value: str | None = None,
    x_unit: str | None = None,
    y_value: str | None = None,
    y_unit: str | None = None,
    z_value: str | None = None,
    z_unit: str | None = None,
) -> ET._Element:
    """
    Returns the MIX SourceSize element.

    :param x_value: The source X value (width) as a string
    :param x_unit: The unit of the source X value (width) as a string
    :param y_value: The source Y value (height) as a string
    :param y_unit: The unit of the source Y value (height) as a string
    :param z_value: The source Z value (depth) as a string
    :param z_unit: The unit of the source z value (depth) as a string

    :returns:
    The following sorted ElementTree structure::

        <mix:SourceSize>
            <mix:SourceXDimension>
                <mix:sourceXDimensionValue>1.23</mix:sourceXDimensionValue>
                <mix:sourceXDimensionUnit>mm.</mix:sourceXDimensionUnit>
            </mix:SourceXDimension>
            <mix:SourceYDimension>
                <mix:sourceYDimensionValue>1.23</mix:sourceXDimensionValue>
                <mix:sourceYDimensionUnit>mm.</mix:sourceXDimensionUnit>
            </mix:SourceYDimension>
            <mix:SourceZDimension>
                <mix:sourceZDimensionValue>1.23</mix:sourceXDimensionValue>
                <mix:sourceZDimensionUnit>mm.</mix:sourceXDimensionUnit>
            </mix:SourceZDimension>
        </mix:SourceSize>

    """

    def _update_dimension(
        value: str | None,
        unit: str | None,
        d: str,
        container: ET._Element,
    ) -> None:
        if value or unit:
            dimension = _subelement(container, f"Source{d}Dimension")
            if value:
                value_el = _subelement(dimension, f"source{d}DimensionValue")
                value_el.text = value
            if unit:
                if unit in DIMENSION_UNITS:
                    unit_el = _subelement(dimension, f"source{d}DimensionUnit")
                    unit_el.text = unit
                else:
                    raise RestrictedElementError(
                        unit, f"source{d}DimensionUnit", DIMENSION_UNITS
                    )

    container = _element("SourceSize")
    for d, v in {
        "X": (x_value, x_unit),
        "Y": (y_value, y_unit),
        "Z": (z_value, z_unit),
    }.items():
        _update_dimension(v[0], v[1], d, container)

    return container


def capture_information(
    created: str | None = None,
    producer: str | list[str] | None = None,
    device: str | None = None,
) -> ET._Element:
    """
    Returns the MIX GeneralCaptureInformation element.

    :param created: The image datetime created as a string
    :param producer: The image producer as a string or list of strings
    :param device: The image creation device classification as a string

    :returns:
    The following sorted ElementTree structure::

        <mix:GeneralCaptureInformation>
            <mix:dateTimeCreated>foo</mix:dateTimeCreated>
            <mix:imageProducer>foo</mix:imageProducer>
            <mix:captureDevice>foo</mix:captureDevice>
        </mix:GeneralCaptureInformation>

    """
    container = _element('GeneralCaptureInformation')

    if created:
        created_el = _subelement(container, 'dateTimeCreated')
        created_el.text = created

    if producer:
        producer = _ensure_list(producer)
        for item in producer:
            producer_el = _subelement(container, 'imageProducer')
            producer_el.text = item

    if device:
        if device in CAPTURE_DEVICE_TYPES:
            device_el = _subelement(container, 'captureDevice')
            device_el.text = device
        else:
            raise RestrictedElementError(
                device, 'captureDevice', CAPTURE_DEVICE_TYPES)

    return container


def device_capture(
    device_type: str,
    manufacturer: str | None = None,
    sensor: str | None = None,
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns either the MIX ScannerCapture or the DigitalCameraCapture
    element depending on the device_type.

    :param device_type: The type of capture device, e.g. 'scanner' or 'camera'
    :param manufacturer: The manufacturer of the capture device as a string
    :param sensor: The type of image sensor of the capture device as a string
    :param child_elements: Child elements as a list

    """
    prefixes = {'scanner': 'scanner',
                'camera': 'digitalCamera'}

    if device_type not in prefixes:
        raise ValueError('Invalid value. Only "scanner" or "camera" are '
                         'valid device types.')

    if child_elements is None:
        child_elements = []

    container = _element(
        'capture',
        prefix=prefixes[device_type][0].capitalize()
        + prefixes[device_type][1:])

    if manufacturer:
        manufacturer_el = _element('manufacturer',
                                   prefix=prefixes[device_type])
        manufacturer_el.text = manufacturer
        child_elements.append(manufacturer_el)

    if sensor and device_type == 'scanner':
        if sensor in SCANNER_SENSOR_TYPES:
            sensor_el = _element('scannerSensor')
            sensor_el.text = sensor
            child_elements.append(sensor_el)
        else:
            raise RestrictedElementError(
                sensor, 'scannerSensor', SCANNER_SENSOR_TYPES)

    if sensor and device_type == 'camera':
        if sensor in CAMERA_SENSOR_TYPES:
            sensor_el = _element('cameraSensor')
            sensor_el.text = sensor
            child_elements.append(sensor_el)
        else:
            raise RestrictedElementError(
                sensor, 'cameraSensor', CAMERA_SENSOR_TYPES)

    if device_type == 'scanner':
        child_elements.sort(key=scanner_capture_order)
    if device_type == 'camera':
        child_elements.sort(key=camera_capture_order)

    for element in child_elements:
        container.append(element)

    return container


def device_model(
    device_type: str,
    name: str | None = None,
    number: str | None = None,
    serialno: str | None = None,
) -> ET._Element:
    """
    Returns either the MIX ScannerModel or the DigitalCameraModel element
    depending on the device_type.

    :param device_type: The type of capture device, e.g. 'scanner' or 'camera'
    :param name: The model name of the capture device as a string
    :param number: The model number of the capture device as a string
    :param serialno: The serial number of the capture device as a string

    """
    prefixes = {'scanner': 'scanner',
                'camera': 'digitalCamera'}

    if device_type not in prefixes:
        raise ValueError('Invalid value. Only "scanner" or "camera" are '
                         'valid device types.')

    container = _element(
        'model',
        prefix=prefixes[device_type][0].capitalize()
        + prefixes[device_type][1:])

    if name:
        device_name_el = _subelement(container, 'modelName',
                                     prefix=prefixes[device_type])
        device_name_el.text = name

    if number:
        device_number_el = _subelement(container, 'modelNumber',
                                       prefix=prefixes[device_type])
        device_number_el.text = number

    if serialno:
        device_serialno_el = _subelement(container, 'modelSerialNo',
                                         prefix=prefixes[device_type])
        device_serialno_el.text = serialno

    return container


def max_optical_resolution(
    x_resolution: int | str | None = None,
    y_resolution: int | str | None = None,
    unit: str | None = None,
) -> ET._Element:
    """
    Returns the MIX MaximumOpticalResolution element.

    :param x_resolution: The x resolution of the scanning sensor as an integer
    :param y_resolution: The y resolution of the scanning sensor as an integer
    :param unit: The unit of the scanning sensor resolution as a string

    :returns:
    The following sorted ElementTree structure::

        <mix:MaximumOpticalResolution>
            <mix:xOpticalResolution>foo</mix:xOpticalResolution>
            <mix:yOpticalResolution>foo</mix:yOpticalResolution>
            <mix:opticalResolutionUnit>foo</mix:opticalResolutionUnit>
        </mix:MaximumOpticalResolution>

    """
    container = _element('MaximumOpticalResolution')

    if x_resolution:
        x_resolution_el = _subelement(container, 'xOpticalResolution')
        x_resolution_el.text = str(x_resolution)

    if y_resolution:
        y_resolution_el = _subelement(container, 'yOpticalResolution')
        y_resolution_el.text = str(y_resolution)

    if unit:
        if unit in OPTICAL_RESOLUTION_UNITS:
            unit_el = _subelement(container, 'opticalResolutionUnit')
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                unit, 'opticalResolutionUnit', OPTICAL_RESOLUTION_UNITS)

    return container


def scanning_software(
    name: str | None = None, version: str | None = None
) -> ET._Element:
    """
    Returns the MIX ScanningSystemSoftware element.

    :param name: The scanning software name as a string
    :version: The scanning software version as a string

    :returns:
    The following sorted ElementTree structure::

        <mix:ScanningSystemSoftware>
            <mix:scanningSoftwareName>foo</mix:scanningSoftwareName>
            <mix:scanningSoftwareVersionNo>foo</mix:scanningSoftwareVersionNo>
        </mix:ScanningSystemSoftware>

    """
    container = _element('ScanningSystemSoftware')

    if name:
        name_el = _subelement(container, 'scanningSoftwareName')
        name_el.text = name

    if version:
        version_el = _subelement(container, 'scanningSoftwareVersionNo')
        version_el.text = version

    return container


def camera_capture_settings(
    child_elements: list[ET._Element] | None = None,
) -> ET._Element:
    """
    Returns the MIX CameraCaptureSettings element.

    :param child_elements: Child elements as a list

    :returns:
    The following sorted ElementTree structure::

        <mix:CameraCaptureSettings>
            {{ Child elements }}
        </mix:CameraCaptureSettings>

    """
    container = _element('CameraCaptureSettings')

    if child_elements:
        child_elements.sort(key=camera_capture_settings_order)

        for element in child_elements:
            container.append(element)

    return container


def image_data(contents: dict[str, str | None] | None = None) -> ET._Element:
    """
    Returns the MIX ImageData element. The function argument contents
    is a dict, that can be retrieved from nisomix.IMAGE_DATA_CONTENTS.
    The keys from contents are matched to create the MIX element and its
    substructure. The dict should look like this::

        contents = {"fnumber": None,
                    "exposure_time": None,
                    "exposure_program": None,
                    "spectral_sensitivity": None,
                    "isospeed_ratings": None,
                    "oecf": None,
                    "exif_version": None,
                    "shutter_speed_value": None,
                    "aperture_value": None,
                    "brightness_value": None,
                    "exposure_bias_value": None,
                    "max_aperture_value": None,
                    "distance": None,
                    "min_distance": None,
                    "max_distance": None,
                    "metering_mode": None,
                    "light_source": None,
                    "flash": None,
                    "focal_length": None,
                    "flash_energy": None,
                    "back_light": None,
                    "exposure_index": None,
                    "sensing_method": None,
                    "cfa_pattern": None,
                    "auto_focus": None,
                    "x_print_aspect_ratio": None,
                    "y_print_aspect_ratio": None}

    """
    if contents is None:
        contents = {}

    tags = {
        'fnumber': 'fNumber', 'exposure_time': 'exposureTime',
        'exposure_program': 'exposureProgram',
        'isospeed_ratings': 'isoSpeedRatings',
        'exif_version': 'exifVersion',
        'metering_mode': 'meteringMode',
        'light_source': 'lightSource', 'flash': 'flash',
        'focal_length': 'focalLength',
        'back_light': 'backLight', 'exposure_index': 'exposureIndex',
        'sensing_method': 'sensingMethod', 'cfa_pattern': 'cfaPattern',
        'auto_focus': 'autoFocus'}

    rationals = {'oecf': 'oECF', 'shutter_speed_value': 'shutterSpeedValue',
                 'aperture_value': 'apertureValue',
                 'brightness_value': 'brightnessValue',
                 'exposure_bias_value': 'exposureBiasValue',
                 'max_aperture_value': 'maxApertureValue',
                 'flash_energy': 'flashEnergy'}

    for key in contents:
        if key not in IMAGE_DATA_CONTENTS:
            raise ValueError('Key "%s" not in supported keys for '
                             'image_data.' % key)

    container = _element('ImageData')
    child_elements = []

    for key, value in contents.items():
        if key in tags and value:
            elem = _element(tags[key])
            elem.text = str(value)
            child_elements.append(elem)

        if key in rationals and value:
            elem = _rationaltype_element(rationals[key], value)
            child_elements.append(elem)

    if contents.get("spectral_sensitivity"):
        spect_sens = _ensure_list(contents["spectral_sensitivity"])
        for item in spect_sens:
            spect_sens_el = _element('spectralSensitivity')
            spect_sens_el.text = item
            child_elements.append(spect_sens_el)

    if contents.get("distance") or contents.get("min_distance") \
            or contents.get("max_distance"):
        subject_distance = _element('SubjectDistance')
        child_elements.append(subject_distance)
    if contents.get("distance"):
        distance_el = _subelement(subject_distance, 'distance')
        distance_el.text = contents["distance"]
    if contents.get("min_distance") or contents.get("max_distance"):
        min_max_distance = _subelement(subject_distance, 'MinMaxDistance')
    if contents.get("min_distance"):
        min_distance_el = _subelement(min_max_distance, 'minDistance')
        min_distance_el.text = contents["min_distance"]
    if contents.get("max_distance"):
        max_distance_el = _subelement(min_max_distance, 'maxDistance')
        max_distance_el.text = contents["max_distance"]

    if contents.get("x_print_aspect_ratio") or \
            contents.get("y_print_aspect_ratio"):
        print_ratio = _element('PrintAspectRatio')
        child_elements.append(print_ratio)
    if contents.get("x_print_aspect_ratio"):
        x_print_aspect_ratio_el = _subelement(print_ratio, 'xPrintAspectRatio')
        x_print_aspect_ratio_el.text = contents["x_print_aspect_ratio"]
    if contents.get("y_print_aspect_ratio"):
        y_print_aspect_ratio_el = _subelement(print_ratio, 'yPrintAspectRatio')
        y_print_aspect_ratio_el.text = contents["y_print_aspect_ratio"]

    child_elements.sort(key=image_data_order)

    for element in child_elements:
        container.append(element)

    return container


def gps_data(
    contents: dict[str, str | int | None] | None = None,
) -> ET._Element:
    """
    Returns the MIX GPSData element. The function argument contents
    is a dict, from nisomix.GPS_DATA_CONTENTS. The keys from the
    contents dict are matched to create the MIX element and its
    substructure. The dict should look like this::

        contents = {"version_id": None,
                    "lat_ref": None,
                    "lat_degrees": None,
                    "lat_minutes": None,
                    "lat_seconds": None,
                    "long_ref": None,
                    "long_degrees": None,
                    "long_minutes": None,
                    "long_seconds": None,
                    "altitude_ref": None,
                    "altitude": None,
                    "timestamp": None,
                    "satellites": None,
                    "status": None,
                    "measure_mode": None,
                    "dop": None,
                    "speed_ref": None,
                    "speed": None,
                    "track_ref": None,
                    "track": None,
                    "img_direction_ref": None,
                    "direction": None,
                    "map_datum": None,
                    "dest_lat_ref": None,
                    "dest_lat_degrees": None,
                    "dest_lat_minutes": None,
                    "dest_lat_seconds": None,
                    "dest_long_ref": None,
                    "dest_long_degrees": None,
                    "dest_long_minutes": None,
                    "dest_long_seconds": None,
                    "dest_bearing_ref": None,
                    "dest_bearing": None,
                    "dest_distance_ref": None,
                    "dest_distance": None,
                    "processing_method": None,
                    "area_information": None,
                    "datestamp": None,
                    "differential": None,
                    "gps_groups": None}

    """
    if contents is None:
        contents = {}

    tags = {'version_id': 'gpsVersionID', 'lat_ref': 'gpsLatitudeRef',
            'long_ref': 'gpsLongitudeRef',
            'altitude_ref': 'gpsAltitudeRef',
            'timestamp': 'gpsTimeStamp', 'satellites': 'gpsSatellites',
            'status': 'gpsStatus',
            'measure_mode': 'gpsMeasureMode',
            'speed_ref': 'gpsSpeedRef',
            'track_ref': 'gpsTrackRef',
            'img_direction_ref': 'gpsImgDirectionRef',
            'map_datum': 'gpsMapDatum',
            'dest_lat_ref': 'gpsDestLatitudeRef',
            'dest_long_ref': 'gpsDestLongitudeRef',
            'dest_bearing_ref': 'gpsDestBearingRef',
            'dest_distance_ref': 'gpsDestDistanceRef',
            'processing_method': 'gpsProcessingMethod',
            'area_information': 'gpsAreaInformation',
            'datestamp': 'gpsDateStamp',
            'differential': 'gpsDifferential'}

    rationals = {'altitude': 'gpsAltitude',
                 'dop': 'gpsDOP',
                 'speed': 'gpsSpeed',
                 'track': 'gpsTrack',
                 'direction': 'gpsImgDirection',
                 'dest_bearing': 'gpsDestBearing',
                 'dest_distance': 'gpsDestDistance'}

    for key in contents:
        if key not in GPS_DATA_CONTENTS:
            raise ValueError('Key "%s" not in supported keys '
                             'for gps_data.' % key)

    container = _element('GPSData')
    child_elements = []

    for key, value in contents.items():
        if key in tags and value:
            elem = _element(tags[key])
            elem.text = str(value)
            child_elements.append(elem)

        if key in rationals and value:
            elem = _rationaltype_element(rationals[key], value)
            child_elements.append(elem)

    if contents.get("lat_degrees") or contents.get("lat_minutes") or \
            contents.get("lat_seconds"):
        lat_group = _gps_group('GPSLatitude', degrees=contents["lat_degrees"],
                               minutes=contents["lat_minutes"],
                               seconds=contents["lat_seconds"])
        child_elements.append(lat_group)

    if contents.get("long_degrees") or contents.get("long_minutes") or \
            contents.get("long_seconds"):
        long_group = _gps_group('GPSLongitude',
                                degrees=contents["long_degrees"],
                                minutes=contents["long_minutes"],
                                seconds=contents["long_seconds"])
        child_elements.append(long_group)

    if contents.get("dest_lat_degrees") or \
            contents.get("dest_lat_minutes") or \
            contents.get("dest_lat_seconds"):
        dest_lat_group = _gps_group('GPSDestLatitude',
                                    degrees=contents["dest_lat_degrees"],
                                    minutes=contents["dest_lat_minutes"],
                                    seconds=contents["dest_lat_seconds"])
        child_elements.append(dest_lat_group)

    if contents.get("dest_long_degrees") or \
            contents.get("dest_long_minutes") or \
            contents.get("dest_long_seconds"):
        dest_long_group = _gps_group('GPSDestLongitude',
                                     degrees=contents["dest_long_degrees"],
                                     minutes=contents["dest_long_minutes"],
                                     seconds=contents["dest_long_seconds"])
        child_elements.append(dest_long_group)

    child_elements.sort(key=gps_data_order)

    for element in child_elements:
        container.append(element)

    return container


def _gps_group(
    tag: str,
    degrees: int | str | list[int | str] | None = None,
    minutes: int | str | list[int | str] | None = None,
    seconds: int | str | list[int | str] | None = None,
) -> ET._Element:
    """
    Returns the MIX gpsGroup type element.

    :param tag: the tag name of the container element
    :param degrees: The degrees of the coordinates as a list (or integer)
    :param minutes: The minutes of the coordinates as a list (or integer)
    :param seconds: The seconds of the coordinates as a list (or integer)

    :returns:
    The following ElementTree structure::

        <mix:{{ tag }}>
            <mix:degrees>
              <mix:numerator>2</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:degrees>
            <mix:minutes>
              <mix:numerator>2</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:minutes>
            <mix:seconds>
              <mix:numerator>2</mix:numerator>
              <mix:denominator>1</mix:denominator>
            </mix:seconds>
        </mix:{{ tag }}>

    """
    container = _element(tag)

    if degrees:
        degrees_el = _rationaltype_element('degrees', degrees)
        container.append(degrees_el)

    if minutes:
        minutes_el = _rationaltype_element('minutes', minutes)
        container.append(minutes_el)

    if seconds:
        seconds_el = _rationaltype_element('seconds', seconds)
        container.append(seconds_el)

    return container


def parse_datetime_created(elem: ET._Element) -> str | None:
    """
    Returns the dateTimeCreated from a MIX metadata
    block in XML.

    :param elem: An ElementTree strucure
    :returns: The datetime created as a string
    """
    created = None

    if elem.tag != (mix_ns, 'dateTimeCreated'):
        elem = elem.xpath('//mix:dateTimeCreated', namespaces=NAMESPACES)[0]

    if elem is not None and elem.text:
        created = elem.text

    return created
