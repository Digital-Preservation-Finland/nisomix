"""Test nisomix.capture_metadata_base module functions."""
from __future__ import unicode_literals

import pytest

import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.base import _element
from nisomix.capture_metadata_base import (_gps_group, camera_capture_settings,
                                           capture_information, device_capture,
                                           device_model, gps_data,
                                           image_capture_metadata, image_data,
                                           max_optical_resolution,
                                           parse_datetime_created,
                                           scanning_software, source_id,
                                           source_information, source_size)
from nisomix.utils import RestrictedElementError


def test_capture_metadata():
    """
    Tests that the element ImageCaptureMetadata is created correctly
    and that the subelements are properly sorted.
    """
    source = _element('SourceInformation')
    capture = _element('GeneralCaptureInformation')
    scanner = _element('ScannerCapture')
    camera = _element('DigitalCameraCapture')
    mix = image_capture_metadata(orientation='unknown', methodology='2',
                                 child_elements=[camera, capture, scanner,
                                                 source])

    xml_str = ('<mix:ImageCaptureMetadata '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:SourceInformation/><mix:GeneralCaptureInformation/>'
               '<mix:ScannerCapture/><mix:DigitalCameraCapture/>'
               '<mix:orientation>unknown</mix:orientation><mix:methodology>2'
               '</mix:methodology></mix:ImageCaptureMetadata>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_orientation_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        image_capture_metadata(orientation='foo')


def test_source_information():
    """Tests that the element SourceInformation is created correctly."""
    s_id = _element('SourceID')
    size = _element('SourceSize')
    mix = source_information(source_type='test',
                             child_elements=[size, s_id])

    xml_str = ('<mix:SourceInformation xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:sourceType>test</mix:sourceType><mix:SourceID/>'
               '<mix:SourceSize/></mix:SourceInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_source_id():
    """Tests that the element SourceID is created correctly."""
    mix = source_id(source_idtype='local', source_idvalue='test')

    xml_str = ('<mix:SourceID xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:sourceIDType>local</mix:sourceIDType>'
               '<mix:sourceIDValue>test</mix:sourceIDValue>'
               '</mix:SourceID>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_source_size():
    """Tests that the element SourceSize is created correctly."""
    mix = source_size(x_value='1', x_unit='mm', y_value='2', y_unit='mm',
                      z_value='3', z_unit='mm')

    xml_str = ('<mix:SourceSize xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:SourceXDimension><mix:sourceXDimensionValue>1'
               '</mix:sourceXDimensionValue><mix:sourceXDimensionUnit>mm'
               '</mix:sourceXDimensionUnit></mix:SourceXDimension>'
               '<mix:SourceYDimension><mix:sourceYDimensionValue>2'
               '</mix:sourceYDimensionValue><mix:sourceYDimensionUnit>mm'
               '</mix:sourceYDimensionUnit></mix:SourceYDimension>'
               '<mix:SourceZDimension><mix:sourceZDimensionValue>3'
               '</mix:sourceZDimensionValue><mix:sourceZDimensionUnit>mm'
               '</mix:sourceZDimensionUnit></mix:SourceZDimension>'
               '</mix:SourceSize>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


@pytest.mark.parametrize(('x_unit', 'y_unit', 'z_unit'), [
    ('foo', 'mm', 'mm'),
    ('mm', 'foo', 'mm'),
    ('mm', 'mm', 'foo')
    ])
def test_source_size_error(x_unit, y_unit, z_unit):
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        source_size(x_unit=x_unit, y_unit=y_unit, z_unit=z_unit)


def test_capture_information():
    """
    Tests that the element GeneralCaptureInformation is created
    correctly.
    """
    mix = capture_information(created='2019', producer=['test', 'test2'],
                              device='still from video')

    xml_str = ('<mix:GeneralCaptureInformation '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:dateTimeCreated>2019</mix:dateTimeCreated>'
               '<mix:imageProducer>test</mix:imageProducer>'
               '<mix:imageProducer>test2</mix:imageProducer>'
               '<mix:captureDevice>still from video</mix:captureDevice>'
               '</mix:GeneralCaptureInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_capture_information_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        capture_information(device='foo')


def test_capture_info_listelem():
    """Tests that certain variables work as both lists and strings."""

    mix = capture_information(producer=["4", "4b"])
    xml_str = ('<mix:GeneralCaptureInformation '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:imageProducer>4</mix:imageProducer>'
               '<mix:imageProducer>4b</mix:imageProducer>'
               '</mix:GeneralCaptureInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    mix = capture_information(producer="4")
    xml_str = ('<mix:GeneralCaptureInformation '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:imageProducer>4</mix:imageProducer>'
               '</mix:GeneralCaptureInformation>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_device_capture_scanner():
    """
    Tests that the element ScannerCapture is created correctly using
    the device_capture function.
    """
    model = _element('ScannerModel')
    max_res = _element('MaximumOpticalResolution')
    software = _element('ScanningSystemSoftware')
    mix = device_capture(device_type='scanner', manufacturer='acme',
                         sensor='undefined',
                         child_elements=[software, model, max_res])

    xml_str = ('<mix:ScannerCapture '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:scannerManufacturer>acme</mix:scannerManufacturer>'
               '<mix:ScannerModel/><mix:MaximumOpticalResolution/>'
               '<mix:scannerSensor>undefined</mix:scannerSensor>'
               '<mix:ScanningSystemSoftware/>'
               '</mix:ScannerCapture>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_device_capture_camera():
    """
    Tests that the element DigitalCameraCapture is created correctly
    using the device_capture function.
    """
    model = _element('DigitalCameraModel')
    settings = _element('CameraCaptureSettings')
    mix = device_capture(device_type='camera', manufacturer='acme',
                         sensor='undefined',
                         child_elements=[settings, model])

    xml_str = ('<mix:DigitalCameraCapture '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:digitalCameraManufacturer>acme'
               '</mix:digitalCameraManufacturer>'
               '<mix:DigitalCameraModel/>'
               '<mix:cameraSensor>undefined</mix:cameraSensor>'
               '<mix:CameraCaptureSettings/>'
               '</mix:DigitalCameraCapture>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_device_capture_error():
    """
    Tests that the invalid values for device type raises an
    exception.
    """
    with pytest.raises(ValueError):
        device_capture(device_type='foo')


def test_sensor_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        device_capture(device_type='scanner', sensor='foo')

    with pytest.raises(RestrictedElementError):
        device_capture(device_type='camera', sensor='foo')


def test_device_model_scanner():
    """
    Tests that the element ScannerModel is created correctly
    using the device_model function.
    """
    mix = device_model(device_type='scanner', name='test', number='2',
                       serialno='3')

    xml_str = ('<mix:ScannerModel '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:scannerModelName>test'
               '</mix:scannerModelName>'
               '<mix:scannerModelNumber>2'
               '</mix:scannerModelNumber>'
               '<mix:scannerModelSerialNo>3'
               '</mix:scannerModelSerialNo>'
               '</mix:ScannerModel>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_device_model_camera():
    """
    Tests that the element DigitalCameraModel is created correctly
    using the device_model function.
    """
    mix = device_model(device_type='camera', name='test', number='2',
                       serialno='3')

    xml_str = ('<mix:DigitalCameraModel '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:digitalCameraModelName>test'
               '</mix:digitalCameraModelName>'
               '<mix:digitalCameraModelNumber>2'
               '</mix:digitalCameraModelNumber>'
               '<mix:digitalCameraModelSerialNo>3'
               '</mix:digitalCameraModelSerialNo>'
               '</mix:DigitalCameraModel>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_device_model_error():
    """
    Tests that the invalid values for device type raises an
    exception.
    """
    with pytest.raises(ValueError):
        device_model(device_type='foo')


def test_max_optical_resolution():
    """
    Tests that the element MaximumOpticalResolution is created
    correctly.
    """
    mix = max_optical_resolution(x_resolution=1, y_resolution=2,
                                 unit='cm')

    xml_str = ('<mix:MaximumOpticalResolution '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:xOpticalResolution>1'
               '</mix:xOpticalResolution>'
               '<mix:yOpticalResolution>2'
               '</mix:yOpticalResolution>'
               '<mix:opticalResolutionUnit>cm'
               '</mix:opticalResolutionUnit>'
               '</mix:MaximumOpticalResolution>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_optical_resolution_error():
    """
    Tests that invalid values for restricted elements return an
    exception.
    """

    with pytest.raises(RestrictedElementError):
        max_optical_resolution(unit='foo')


def test_scanning_software():
    """
    Tests that the element ScanningSystemSoftware is created
    correctly.
    """
    mix = scanning_software(name='1', version='2')

    xml_str = ('<mix:ScanningSystemSoftware '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:scanningSoftwareName>1'
               '</mix:scanningSoftwareName>'
               '<mix:scanningSoftwareVersionNo>2'
               '</mix:scanningSoftwareVersionNo>'
               '</mix:ScanningSystemSoftware>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_camera_capture_settings():
    """
    Tests that the element CameraCaptureSettings is created correctly
    and that the subelements are sorted properly.
    """
    gps = _element('GPSData')
    img = _element('ImageData')

    mix = camera_capture_settings(child_elements=[gps, img])

    xml_str = ('<mix:CameraCaptureSettings '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:ImageData/><mix:GPSData/>'
               '</mix:CameraCaptureSettings>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_data():
    """Tests that the element ImageData is created correctly."""

    contents = {"fnumber": "1",
                "exposure_time": "2",
                "exposure_program": "3",
                "spectral_sensitivity": ["4", "4b"],
                "isospeed_ratings": 5,
                "oecf": 6,
                "exif_version": "7",
                "shutter_speed_value": 8,
                "aperture_value": 9,
                "brightness_value": 10,
                "exposure_bias_value": 11,
                "max_aperture_value": 12,
                "distance": "13",
                "min_distance": "14",
                "max_distance": "15",
                "metering_mode": "16",
                "light_source": "17",
                "flash": "18",
                "focal_length": "19",
                "flash_energy": 20,
                "back_light": "21",
                "exposure_index": "22",
                "sensing_method": "23",
                "cfa_pattern": 24,
                "auto_focus": "25",
                "x_print_aspect_ratio": "26",
                "y_print_aspect_ratio": "27"}

    mix = image_data(contents=contents)

    xml_str = ('<mix:ImageData '
               'xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:fNumber>1</mix:fNumber><mix:exposureTime>2'
               '</mix:exposureTime><mix:exposureProgram>3'
               '</mix:exposureProgram>'
               '<mix:spectralSensitivity>4</mix:spectralSensitivity>'
               '<mix:spectralSensitivity>4b</mix:spectralSensitivity>'
               '<mix:isoSpeedRatings>5</mix:isoSpeedRatings>'
               '<mix:oECF><mix:numerator>6</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:oECF>'
               '<mix:exifVersion>7</mix:exifVersion>'
               '<mix:shutterSpeedValue><mix:numerator>8</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:shutterSpeedValue><mix:apertureValue>'
               '<mix:numerator>9</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:apertureValue><mix:brightnessValue>'
               '<mix:numerator>10</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:brightnessValue><mix:exposureBiasValue>'
               '<mix:numerator>11</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:exposureBiasValue><mix:maxApertureValue>'
               '<mix:numerator>12</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:maxApertureValue><mix:SubjectDistance>'
               '<mix:distance>13</mix:distance><mix:MinMaxDistance>'
               '<mix:minDistance>14</mix:minDistance>'
               '<mix:maxDistance>15</mix:maxDistance>'
               '</mix:MinMaxDistance></mix:SubjectDistance>'
               '<mix:meteringMode>16</mix:meteringMode>'
               '<mix:lightSource>17</mix:lightSource><mix:flash>18</mix:flash>'
               '<mix:focalLength>19</mix:focalLength><mix:flashEnergy>'
               '<mix:numerator>20</mix:numerator>'
               '<mix:denominator>1</mix:denominator>'
               '</mix:flashEnergy><mix:backLight>21</mix:backLight>'
               '<mix:exposureIndex>22</mix:exposureIndex>'
               '<mix:sensingMethod>23</mix:sensingMethod>'
               '<mix:cfaPattern>24</mix:cfaPattern>'
               '<mix:autoFocus>25</mix:autoFocus><mix:PrintAspectRatio>'
               '<mix:xPrintAspectRatio>26</mix:xPrintAspectRatio>'
               '<mix:yPrintAspectRatio>27</mix:yPrintAspectRatio>'
               '</mix:PrintAspectRatio></mix:ImageData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_data_listelem():
    """Tests that certain variables work as both lists and strings."""

    contents = {"spectral_sensitivity": ["4", "4b"]}
    mix = image_data(contents=contents)
    xml_str = ('<mix:ImageData xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:spectralSensitivity>4</mix:spectralSensitivity>'
               '<mix:spectralSensitivity>4b</mix:spectralSensitivity>'
               '</mix:ImageData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))

    contents = {"spectral_sensitivity": "4"}
    mix = image_data(contents=contents)
    xml_str = ('<mix:ImageData xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:spectralSensitivity>4</mix:spectralSensitivity>'
               '</mix:ImageData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_data_empty_key():
    """Tests that key with value None do not create elements."""
    contents = {"spectral_sensitivity": None}
    mix = image_data(contents=contents)
    xml_str = ('<mix:ImageData xmlns:mix="http://www.loc.gov/mix/v20">'
               '</mix:ImageData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_image_data_dict_error():
    """Tests that unwanted keys in dict return an exception."""
    with pytest.raises(ValueError):
        contents = {'foo': 'bar'}
        image_data(contents=contents)


def test_gps_group():
    """Test that the element group gpsGroup is
    created correctly.
    """

    mix = _gps_group('testGroup', degrees=[1], minutes=[2, 3], seconds=4)

    xml_str = ('<mix:testGroup xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:degrees><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:degrees>'
               '<mix:minutes><mix:numerator>2</mix:numerator>'
               '<mix:denominator>3</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>4</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:testGroup>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gps_data():
    """Test that the element GPSData is
    created correctly.
    """

    contents = {"version_id": "1",
                "lat_ref": "2",
                "lat_degrees": 3,
                "lat_minutes": 4,
                "lat_seconds": 5,
                "long_ref": "6",
                "long_degrees": 7,
                "long_minutes": 8,
                "long_seconds": 9,
                "altitude_ref": "10",
                "altitude": 11,
                "timestamp": "12",
                "satellites": "13",
                "status": "14",
                "measure_mode": "15",
                "dop": 16,
                "speed_ref": "17",
                "speed": 18,
                "track_ref": "19",
                "track": 20,
                "img_direction_ref": "21",
                "direction": 22,
                "map_datum": "23",
                "dest_lat_ref": "24",
                "dest_lat_degrees": 25,
                "dest_lat_minutes": 26,
                "dest_lat_seconds": 27,
                "dest_long_ref": "28",
                "dest_long_degrees": 29,
                "dest_long_minutes": 30,
                "dest_long_seconds": 31,
                "dest_bearing_ref": "32",
                "dest_bearing": 33,
                "dest_distance_ref": "34",
                "dest_distance": [35, 3],
                "processing_method": "36",
                "area_information": "37",
                "datestamp": "38",
                "differential": "39",
                "gps_groups": "40"}

    mix = gps_data(contents=contents)

    xml_str = ('<mix:GPSData xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:gpsVersionID>1</mix:gpsVersionID><mix:gpsLatitudeRef>2'
               '</mix:gpsLatitudeRef><mix:GPSLatitude><mix:degrees>'
               '<mix:numerator>3</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:degrees><mix:minutes><mix:numerator>4'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:minutes><mix:seconds><mix:numerator>5</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSLatitude><mix:gpsLongitudeRef>6</mix:gpsLongitudeRef>'
               '<mix:GPSLongitude><mix:degrees><mix:numerator>7'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:degrees><mix:minutes><mix:numerator>8</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>9</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSLongitude><mix:gpsAltitudeRef>10</mix:gpsAltitudeRef>'
               '<mix:gpsAltitude><mix:numerator>11</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsAltitude>'
               '<mix:gpsTimeStamp>12</mix:gpsTimeStamp><mix:gpsSatellites>13'
               '</mix:gpsSatellites><mix:gpsStatus>14</mix:gpsStatus>'
               '<mix:gpsMeasureMode>15</mix:gpsMeasureMode><mix:gpsDOP>'
               '<mix:numerator>16</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:gpsDOP><mix:gpsSpeedRef>17'
               '</mix:gpsSpeedRef><mix:gpsSpeed><mix:numerator>18'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:gpsSpeed><mix:gpsTrackRef>19</mix:gpsTrackRef>'
               '<mix:gpsTrack><mix:numerator>20</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsTrack>'
               '<mix:gpsImgDirectionRef>21</mix:gpsImgDirectionRef>'
               '<mix:gpsImgDirection><mix:numerator>22</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsImgDirection>'
               '<mix:gpsMapDatum>23</mix:gpsMapDatum>'
               '<mix:gpsDestLatitudeRef>24</mix:gpsDestLatitudeRef>'
               '<mix:GPSDestLatitude><mix:degrees><mix:numerator>25'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:degrees><mix:minutes><mix:numerator>26</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>27</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSDestLatitude><mix:gpsDestLongitudeRef>28'
               '</mix:gpsDestLongitudeRef><mix:GPSDestLongitude>'
               '<mix:degrees><mix:numerator>29</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:degrees>'
               '<mix:minutes><mix:numerator>30</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>31</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSDestLongitude><mix:gpsDestBearingRef>32'
               '</mix:gpsDestBearingRef><mix:gpsDestBearing><mix:numerator>33'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:gpsDestBearing><mix:gpsDestDistanceRef>34'
               '</mix:gpsDestDistanceRef><mix:gpsDestDistance>'
               '<mix:numerator>35</mix:numerator><mix:denominator>3'
               '</mix:denominator></mix:gpsDestDistance>'
               '<mix:gpsProcessingMethod>36</mix:gpsProcessingMethod>'
               '<mix:gpsAreaInformation>37</mix:gpsAreaInformation>'
               '<mix:gpsDateStamp>38</mix:gpsDateStamp><mix:gpsDifferential>39'
               '</mix:gpsDifferential></mix:GPSData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gps_data_empty_key():
    """Tests that key with value None do not create elements."""
    contents = {"lat_degrees": None}
    mix = gps_data(contents=contents)
    xml_str = ('<mix:GPSData xmlns:mix="http://www.loc.gov/mix/v20">'
               '</mix:GPSData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gps_data_dict_error():
    """Tests that unwanted keys in dict return an exception."""
    with pytest.raises(ValueError):
        contents = {'foo': 'bar'}
        gps_data(contents=contents)


def test_parse_datetime_created():
    """Tests the parse_datetime_created function."""

    xml_str = ('<mix:mix xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:GeneralCaptureInformation>'
               '<mix:dateTimeCreated>2019-04-29T10:10:05</mix:dateTimeCreated>'
               '<mix:imageProducer>test</mix:imageProducer>'
               '<mix:imageProducer>test2</mix:imageProducer>'
               '<mix:captureDevice>still from video</mix:captureDevice>'
               '</mix:GeneralCaptureInformation></mix:mix>')

    assert parse_datetime_created(
        ET.fromstring(xml_str)) == '2019-04-29T10:10:05'
