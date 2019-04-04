"""Functions for reading and generating MIX Data Dictionaries as
xml.etree.ElementTree data structures.
"""

import six
from nisomix.base import _element, _subelement, _rationaltype_element
from nisomix.utils import (ORIENTATION_TYPES, DIMENSION_UNITS,
                           CAPTURE_DEVICE_TYPES, SCANNER_SENSOR_TYPES,
                           OPTICAL_RESOLUTION_UNITS, CAMERA_SENSOR_TYPES,
                           IMAGE_DATA_CONTENTS, GPS_DATA_CONTENTS,
                           image_capture_order, scanner_capture_order,
                           camera_capture_order, camera_capture_settings_order,
                           RestrictedElementError,
                           image_data_order, gps_data_order)


def image_capture_metadata(orientation=None, methodology=None,
                           child_elements=None):
    """Returns MIX ImageCaptureMetadata element

    Returns the following sorted ElementTree structure::

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
                'The value "%s" is invalid for orientation, accepted values '
                'are: "%s".' % (orientation, '", "'.join(ORIENTATION_TYPES)))
    if methodology:
        methodology_el = _element('methodology')
        methodology_el.text = methodology
        child_elements.append(methodology_el)

    child_elements.sort(key=image_capture_order)

    for element in child_elements:
        container.append(element)

    return container


def source_information(source_type=None, child_elements=None):
    """Returns MIX SourceInformation element

    Returns the following sorted ElementTree structure::

        <mix:SourceInformation>
          <mix:sourceType>foo</mix:sourceType>
          {{ Child elements }}
        </mix:SourceInformation>

    """
    container = _element('SourceInformation')

    if source_type:
        source_type_el = _subelement(container, 'sourceType')
        source_type_el.text = source_type

    for element in child_elements:
        container.append(element)

    return container


def source_id(source_idtype=None, source_idvalue=None):
    """Returns MIX SourceID element

    Returns the following sorted ElementTree structure::

        <mix:SourceID>
          <mix:sourceIDType>foo</mix:sourceIDType>
          <mix:sourceIDValue>foo</mix:sourceIDValue>
          {{ Child elements }}
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
def source_size(x_value=None, x_unit=None, y_value=None, y_unit=None,
                z_value=None, z_unit=None):
    """Returns MIX SourceSize element

    Returns the following sorted ElementTree structure::

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
    container = _element('SourceSize')

    if x_value or x_unit:
        x_dimension = _subelement(container, 'SourceXDimension')
        if x_value:
            x_value_el = _subelement(x_dimension, 'sourceXDimensionValue')
            x_value_el.text = x_value
        if x_unit:
            if x_unit in DIMENSION_UNITS:
                x_unit_el = _subelement(x_dimension, 'sourceXDimensionUnit')
                x_unit_el.text = x_unit
            else:
                raise RestrictedElementError(
                    'The value "%s" is invalid for sourceXDimensionUnit, '
                    'accepted values are: "%s".' % (
                        x_unit, '", "'.join(DIMENSION_UNITS)))

    if y_value or y_unit:
        y_dimension = _subelement(container, 'SourceYDimension')
        if y_value:
            y_value_el = _subelement(y_dimension, 'sourceYDimensionValue')
            y_value_el.text = y_value
        if y_unit:
            if y_unit in DIMENSION_UNITS:
                y_unit_el = _subelement(y_dimension, 'sourceYDimensionUnit')
                y_unit_el.text = y_unit
            else:
                raise RestrictedElementError(
                    'The value "%s" is invalid for sourceYDimensionUnit, '
                    'accepted values are: "%s".' % (
                        y_unit, '", "'.join(DIMENSION_UNITS)))

    if z_value or z_unit:
        z_dimension = _subelement(container, 'SourceZDimension')
        if z_value:
            z_value_el = _subelement(z_dimension, 'sourceZDimensionValue')
            z_value_el.text = z_value
        if z_unit:
            if z_unit in DIMENSION_UNITS:
                z_unit_el = _subelement(z_dimension, 'sourceZDimensionUnit')
                z_unit_el.text = z_unit
            else:
                raise RestrictedElementError(
                    'The value "%s" is invalid for sourceZDimensionUnit, '
                    'accepted values are: "%s".' % (
                        z_unit, '", "'.join(DIMENSION_UNITS)))

    return container


def capture_information(created=None, producer=None, device=None):
    """Returns MIX GeneralCaptureInformation element

    Returns the following sorted ElementTree structure::

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
        if not isinstance(producer, list):
            producer = [producer]
        for item in producer:
            producer_el = _subelement(container, 'imageProducer')
            producer_el.text = item

    if device:
        if device in CAPTURE_DEVICE_TYPES:
            device_el = _subelement(container, 'captureDevice')
            device_el.text = device
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for captureDevice, accepted '
                'values are: "%s".' % (
                    device, '", "'.join(CAPTURE_DEVICE_TYPES)))

    return container


def device_capture(device_type, manufacturer=None, sensor=None,
                   child_elements=None):
    """
    Returns either MIX ScannerCapture or the DigitalCameraCapture
    element.

    """
    prefixes = {'scanner': 'scanner',
                'camera': 'digitalCamera'}

    if not child_elements:
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
                'The value "%s" is invalid for scannerSensor, accepted '
                'values are: "%s".' % (
                    sensor, '", "'.join(SCANNER_SENSOR_TYPES)))

    if sensor and device_type == 'camera':
        if sensor in CAMERA_SENSOR_TYPES:
            sensor_el = _element('cameraSensor')
            sensor_el.text = sensor
            child_elements.append(sensor_el)
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for cameraSensor, accepted '
                'values are: "%s".' % (
                    sensor, '", "'.join(CAMERA_SENSOR_TYPES)))

    if device_type == 'scanner':
        child_elements.sort(key=scanner_capture_order)
    if device_type == 'camera':
        child_elements.sort(key=camera_capture_order)

    for element in child_elements:
        container.append(element)

    return container


def device_model(device_type, name=None, number=None,
                 serialno=None):
    """
    Returns either the ScannerModel or the DigitalCameraModel element.
    """
    prefixes = {'scanner': 'scanner',
                'camera': 'digitalCamera'}

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


def max_optical_resolution(x_resolution=None, y_resolution=None, unit=None):
    """Returns MIX MaximumOpticalResolution element

    Returns the following sorted ElementTree structure::

        <mix:MaximumOpticalResolution>
          <mix:xOpticalResolution>foo</mix:xOpticalResolution>
          <mix:yOpticalResolution>foo</mix:yOpticalResolution>
          <mix:opticalResolutionUnit>foo</mix:opticalResolutionUnit>
        </mix:MaximumOpticalResolution>

    """
    container = _element('MaximumOpticalResolution')

    if x_resolution:
        x_resolution_el = _subelement(container, 'xOpticalResolution')
        x_resolution_el.text = x_resolution

    if y_resolution:
        y_resolution_el = _subelement(container, 'yOpticalResolution')
        y_resolution_el.text = y_resolution

    if unit:
        if unit in OPTICAL_RESOLUTION_UNITS:
            unit_el = _subelement(container, 'opticalResolutionUnit')
            unit_el.text = unit
        else:
            raise RestrictedElementError(
                'The value "%s" is invalid for opticalResolutionUnit, '
                'accepted values are: "%s".' % (
                    unit, '", "'.join(OPTICAL_RESOLUTION_UNITS)))

    return container


def scanning_software(name=None, version=None):
    """Returns MIX ScanningSystemSoftware element

    Returns the following sorted ElementTree structure::

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


def camera_capture_settings(child_elements=None):
    """Returns MIX CameraCaptureSettings element

    Returns the following sorted ElementTree structure::

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


def image_data(contents=None):
    """
    Returns the MIX ImageData element. The function argument contents
    is a dict. The keys from contents are matched to create the MIX
    element and its substructure. The dict should look like this::

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
    child_elems = []

    for key, value in six.iteritems(contents):
        if key in tags and value:
            elem = _element(tags[key])
            elem.text = value
            child_elems.append(elem)

        if key in rationals and value:
            elem = _rationaltype_element(rationals[key], value)
            child_elems.append(elem)

    if contents.get("spectral_sensitivity"):
        if not isinstance(contents["spectral_sensitivity"], list):
            contents["spectral_sensitivity"] = \
                [contents["spectral_sensitivity"]]
        for item in contents["spectral_sensitivity"]:
            spec_sens_el = _element('spectralSensitivity')
            spec_sens_el.text = item
            child_elems.append(spec_sens_el)

    if contents.get("distance") or contents.get("min_distance") \
            or contents.get("max_distance"):
        subject_distance = _element('SubjectDistance')
        child_elems.append(subject_distance)
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
        child_elems.append(print_ratio)
    if contents.get("x_print_aspect_ratio"):
        x_print_aspect_ratio_el = _subelement(print_ratio, 'xPrintAspectRatio')
        x_print_aspect_ratio_el.text = contents["x_print_aspect_ratio"]
    if contents.get("y_print_aspect_ratio"):
        y_print_aspect_ratio_el = _subelement(print_ratio, 'yPrintAspectRatio')
        y_print_aspect_ratio_el.text = contents["y_print_aspect_ratio"]

    child_elems.sort(key=image_data_order)

    for element in child_elems:
        container.append(element)

    return container


def gps_data(contents=None):
    """
    Returns the MIX GPSData element. The function argument contents
    is a dict, see global variable GPS_DATA_CONTENTS. The keys from
    contents are matched to create the MIX element and its substructure.
    The dict should look like this::

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
    child_elems = []

    for key, value in six.iteritems(contents):
        if key in tags and value:
            elem = _element(tags[key])
            elem.text = value
            child_elems.append(elem)

        if key in rationals and value:
            elem = _rationaltype_element(rationals[key], value)
            child_elems.append(elem)

    if contents.get("lat_degrees") or contents.get("lat_minutes") or \
            contents.get("lat_seconds"):
        lat_group = _gps_group('GPSLatitude', degrees=contents["lat_degrees"],
                               minutes=contents["lat_minutes"],
                               seconds=contents["lat_seconds"])
        child_elems.append(lat_group)

    if contents.get("long_degrees") or contents.get("long_minutes") or \
            contents.get("long_seconds"):
        long_group = _gps_group('GPSLongitude',
                                degrees=contents["long_degrees"],
                                minutes=contents["long_minutes"],
                                seconds=contents["long_seconds"])
        child_elems.append(long_group)

    if contents.get("dest_lat_degrees") or \
            contents.get("dest_lat_minutes") or \
            contents.get("dest_lat_seconds"):
        dest_lat_group = _gps_group('GPSDestLatitude',
                                    degrees=contents["dest_lat_degrees"],
                                    minutes=contents["dest_lat_minutes"],
                                    seconds=contents["dest_lat_seconds"])
        child_elems.append(dest_lat_group)

    if contents.get("dest_long_degrees") or \
            contents.get("dest_long_minutes") or \
            contents.get("dest_long_seconds"):
        dest_long_group = _gps_group('GPSDestLongitude',
                                     degrees=contents["dest_long_degrees"],
                                     minutes=contents["dest_long_minutes"],
                                     seconds=contents["dest_long_seconds"])
        child_elems.append(dest_long_group)

    child_elems.sort(key=gps_data_order)

    for element in child_elems:
        container.append(element)

    return container


def _gps_group(tag, degrees=None, minutes=None, seconds=None):
    """Returns MIX gpsGroup type element.

    Returns the following ElementTree structure::

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
