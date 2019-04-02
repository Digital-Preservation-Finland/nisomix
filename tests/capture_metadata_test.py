"""Test nisomix.capture_metadata functions."""
import pytest
import lxml.etree as ET
import xml_helpers.utils as h
from nisomix.mix import _element
from nisomix.utils import RestrictedElementError
from nisomix.capture_metadata import (image_capture_metadata,
                                      source_information, source_id,
                                      source_size, capture_information,
                                      gps_data,
                                      _gps_group)


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
                             child_elements=[s_id, size])

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


def test_gps_group():
    """Test that the element group gpsGroup is
    created correctly.
    """

    mix = _gps_group('testGroup', degrees='1', minutes='2', seconds='3')

    xml_str = ('<mix:testGroup xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:degrees><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:degrees>'
               '<mix:minutes><mix:numerator>2</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>3</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:testGroup>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))


def test_gps_data():
    """Test that the element GPSData is
    created correctly.
    """

    mix = gps_data(version='1', lat_ref='1', lat_degrees='1', lat_minutes='1',
                   lat_seconds='1', long_ref='1', long_degrees='1',
                   long_minutes='1', long_seconds='1', altitude_ref='1',
                   altitude='1', timestamp='1', satellites='1', status='1',
                   measure_mode='1', dop='1', speed_ref='1', speed='1',
                   track_ref='1', track='1', direction_ref='1', direction='1',
                   map_datum='1', dest_lat_ref='1', dest_lat_degrees='1',
                   dest_lat_minutes='1', dest_lat_seconds='1',
                   dest_long_ref='1', dest_long_degrees='1',
                   dest_long_minutes='1', dest_long_seconds='1',
                   dest_bearing_ref='1', dest_bearing='1',
                   dest_distance_ref='1', dest_distance='1',
                   processing_method='1', area_information='1', datestamp='1',
                   differential='1', gps_groups='1')

    xml_str = ('<mix:GPSData xmlns:mix="http://www.loc.gov/mix/v20">'
               '<mix:gpsVersionID>1</mix:gpsVersionID><mix:gpsLatitudeRef>1'
               '</mix:gpsLatitudeRef><mix:GPSLatitude><mix:degrees>'
               '<mix:numerator>1</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:degrees><mix:minutes><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:minutes><mix:seconds><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSLatitude><mix:gpsLongitudeRef>1</mix:gpsLongitudeRef>'
               '<mix:GPSLongitude><mix:degrees><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:degrees><mix:minutes><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSLongitude><mix:gpsAltitudeRef>1</mix:gpsAltitudeRef>'
               '<mix:gpsAltitude><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsAltitude>'
               '<mix:gpsTimeStamp>1</mix:gpsTimeStamp><mix:gpsSatellites>1'
               '</mix:gpsSatellites><mix:gpsStatus>1</mix:gpsStatus>'
               '<mix:gpsMeasureMode>1</mix:gpsMeasureMode><mix:gpsDOP>'
               '<mix:numerator>1</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:gpsDOP><mix:gpsSpeedRef>1'
               '</mix:gpsSpeedRef><mix:gpsSpeed><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:gpsSpeed><mix:gpsTrackRef>1</mix:gpsTrackRef>'
               '<mix:gpsTrack><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsTrack>'
               '<mix:gpsImgDirectionRef>1</mix:gpsImgDirectionRef>'
               '<mix:gpsImgDirection><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:gpsImgDirection>'
               '<mix:gpsMapDatum>1</mix:gpsMapDatum>'
               '<mix:gpsDestLatitudeRef>1</mix:gpsDestLatitudeRef>'
               '<mix:GPSDestLatitude><mix:degrees><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:degrees><mix:minutes><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSDestLatitude><mix:gpsDestLongitudeRef>1'
               '</mix:gpsDestLongitudeRef><mix:GPSDestLongitude>'
               '<mix:degrees><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:degrees>'
               '<mix:minutes><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:minutes>'
               '<mix:seconds><mix:numerator>1</mix:numerator>'
               '<mix:denominator>1</mix:denominator></mix:seconds>'
               '</mix:GPSDestLongitude><mix:gpsDestBearingRef>1'
               '</mix:gpsDestBearingRef><mix:gpsDestBearing><mix:numerator>1'
               '</mix:numerator><mix:denominator>1</mix:denominator>'
               '</mix:gpsDestBearing><mix:gpsDestDistanceRef>1'
               '</mix:gpsDestDistanceRef><mix:gpsDestDistance>'
               '<mix:numerator>1</mix:numerator><mix:denominator>1'
               '</mix:denominator></mix:gpsDestDistance>'
               '<mix:gpsProcessingMethod>1</mix:gpsProcessingMethod>'
               '<mix:gpsAreaInformation>1</mix:gpsAreaInformation>'
               '<mix:gpsDateStamp>1</mix:gpsDateStamp><mix:gpsDifferential>1'
               '</mix:gpsDifferential></mix:GPSData>')

    assert h.compare_trees(mix, ET.fromstring(xml_str))
