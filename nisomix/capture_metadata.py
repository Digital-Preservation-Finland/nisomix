"""Functions for reading and generating MIX Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * MIX http://www.loc.gov/standards/mix/
    * Schema documentation: Data Dictionary - Technical Metadata for
                            Digital Still Images (ANSI/NISO Z39.87-2006)
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""

import lxml.etree as ET
from xml_helpers.utils import xsi_ns
from nisomix.utils import MIX_NS, NAMESPACES


def mix_ImageCaptureMetadata(sourceType=None, SourceID_elements=None,
                             sourceXDimensionValue=None,
                             sourceXDimensionUnit=None,
                             sourceYDimensionValue=None,
                             sourceYDimensionUnit=None,
                             sourceZDimensionValue=None,
                             sourceZDimensionUnit=None,
                             dateTimeCreated=None, imageProducer_elements=None,
                             captureDevice=None,
                             scannerManufacturer=None, scannerModelName=None,
                             scannerModelNumber=None, scannerModelSerialNo=None,
                             xOpticalResolution=None, yOpticalResolution=None,
                             opticalResolutionUnit=None, scannerSensor=None,
                             scanningSoftwareName=None,
                             scanningSoftwareVersionNo=None,
                             digitalCameraManufacturer=None,
                             DigitalCameraModelName=None,
                             DigitalCameraModelNumber=None,
                             DigitalCameraModelSerialNo=None, cameraSensor=None,
                             fNumber=None,
                             exposureTime=None, exposureProgram=None,
                             spectralSensitivity_elements=None,
                             isoSpeedRatings=None, oECF=None, rationalType=None,
                             exifVersion=None,
                             shutterSpeedValue=None, apertureValue=None,
                             brightnessValue=None,
                             exposureBiasValue=None, maxApertureValue=None,
                             distance=None,
                             minDistance=None, maxDistance=None,
                             meteringMode=None,
                             lightSource=None, flash=None, focalLength=None,
                             flashEnergy=None,
                             backLight=None, exposureIndex=None,
                             sensingMethod=None,
                             cfaPattern=None, autoFocus=None,
                             xPrintAspectRatio=None,
                             yPrintAspectRatio=None, gpsVersionID=None,
                             gpsLatitudeRef=None,
                             GPSLatitude_element=None, gpsLongitudeRef=None,
                             GPSLongitude_element=None, gpsAltitudeRef=None,
                             gpsAltitude=None,
                             gpsTimeStamp=None, gpsSatellites=None,
                             gpsStatus=None,
                             gpsMeasureMode=None, gpsDOP=None, gpsSpeedRef=None,
                             gpsSpeed=None,
                             gpsTrackRef=None, gpsTrack=None,
                             gpsImgDirectionRef=None,
                             gpsImgDirection=None, gpsMapDatum=None,
                             gpsDestLatitudeRef=None,
                             GPSDestLatitude_element=None,
                             gpsDestLongitudeRef=None,
                             GPSDestLongitude_element=None,
                             gpsDestBearingRef=None,
                             gpsDestBearing=None, gpsDestDistanceRef=None,
                             gpsDestDistance=None,
                             gpsProcessingMethod=None, gpsAreaInformation=None,
                             gpsDateStamp=None,
                             gpsDifferential=None, typeOfOrientationType=None,
                             methodology=None):
    """Returns MIX ImageCaptureMetadata element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:ImageCaptureMetadata>
            <mix:SourceInformation>
                <mix:sourceType></mix:sourceType>
                {{ SourceID elements }}
                <mix:SourceSize>
                    <mix:SourceXDimension>
                        <mix:sourceXDimensionValue></mix:sourceXDimensionValue>
                        <mix:sourceXDimensionUnit></mix:sourceXDimensionUnit>
                    </mix:SourceXDimension>
                    <mix:SourceYDimension>
                        <mix:sourceYDimensionValue></mix:sourceYDimensionValue>
                        <mix:sourceYDimensionUnit></mix:sourceYDimensionUnit>
                    </mix:SourceYDimension>
                    <mix:SourceZDimension>
                        <mix:sourceZDimensionValue></mix:sourceZDimensionValue>
                        <mix:sourceZDimensionUnit></mix:sourceZDimensionUnit>
                    </mix:SourceZDimension>
                </mix:SourceSize>
            </mix:SourceInformation>
            <mix:GeneralCaptureInformation>
                <mix:dateTimeCreated></mix:dateTimeCreated>
                {{ imageProducer elements }}
                <mix:captureDevice></mix:captureDevice>
            </mix:GeneralCaptureInformation>
            <mix:ScannerCapture>
                <mix:scannerManufacturer></mix:scannerManufacturer>
                <mix:scannerModel>
                    <mix:scannerModelName></mix:scannerModelName>
                    <mix:scannerModelNumber></mix:scannerModelNumber>
                    <mix:scannerModelSerialNo></mix:scannerModelSerialNo>
                </mix:scannerModel>
                <mix:MaximumOpticalResolution>
                    <mix:xOpticalResolution></mix:xOpticalResolution>
                    <mix:yOpticalResolution></mix:yOpticalResolution>
                    <mix:opticalResolutionUnit></mix:opticalResolutionUnit>
                </mix:MaximumOpticalResolution>
                <mix:scannerSensor></mix:scannerSensor>
                <mix:ScanningSystemSoftware>
                    <mix:scanningSoftwareName></mix:scanningSoftwareName>
                    <mix:scanningSoftwareVersionNo></mix:scanningSoftwareVersionNo>
                </mix:ScanningSystemSoftware>
            </mix:ScannerCapture>
            <mix:DigitalCameraCapture>
                <mix:digitalCameraManufacturer></mix:digitalCameraManufacturer>
                <mix:DigitalCameraModel>
                    <mix:DigitalCameraModelName></mix:DigitalCameraModelName>
                    <mix:DigitalCameraModelNumber></mix:DigitalCameraModelNumber>
                    <mix:DigitalCameraModelSerialNo></mix:DigitalCameraModelSerialNo>
                </mix:DigitalCameraModel>
                <mix:cameraSensor></mix:cameraSensor>
                <mix:CameraCaptureSettings>
                    <mix:ImageData>
                        <mix:fNumber></mix:fNumber>
                        <mix:exposureTime></mix:exposureTime>
                        <mix:spectralSensitivity></mix:spectralSensitivity>
                        <mix:isoSpeedRatings></mix:isoSpeedRatings>
                        <mix:oECF></mix:oECF>
                        <mix:exifVersion></mix:exifVersion>
                        <mix:shutterSpeedValue></mix:shutterSpeedValue>
                        <mix:apertureValue></mix:apertureValue>
                        <mix:brightnessValue></mix:brightnessValue>
                        <mix:exposureBiasValue></mix:exposureBiasValue>
                        <mix:maxApertureValue></mix:maxApertureValue>
                        <mix:SubjectDistance>
                            <mix:distance></mix:distance>
                            <mix:MinMaxDistance>
                                <mix:minDistance></mix:minDistance>
                                <mix:maxDistance></mix:maxDistance>
                            </mix:MinMaxDistance>
                        </mix:SubjectDistance>
                        <mix:meteringMode></mix:meteringMode>
                        <mix:lightSource></mix:lightSource>
                        <mix:flash></mix:flash>
                        <mix:focalLength></mix:focalLength>
                        <mix:flashEnergy></mix:flashEnergy>
                        <mix:backLight></mix:backLight>
                        <mix:exposureIndex></mix:exposureIndex>
                        <mix:sensingMethod></mix:sensingMethod>
                        <mix:cfaPattern></mix:cfaPattern>
                        <mix:autoFocus></mix:autoFocus>
                        <mix:PrintAspectRatio>
                            <mix:xPrintAspectRatio></mix:xPrintAspectRatio>
                            <mix:yPrintAspectRatio></mix:yPrintAspectRatio>
                        </mix:PrintAspectRatio>
                        <mix:GPSData>
                            <mix:gpsVersionID></mix:gpsVersionID>
                            <mix:gpsLatitudeRef></mix:gpsLatitudeRef>
                            {{ GPSLatitude gpsGroup element }}
                            <mix:gpsLongitudeRef></mix:gpsLongitudeRef>
                            {{ GPSLongitude gpsGroup element }}
                            <mix:gpsAltitudeRef></mix:gpsAltitudeRef>
                            <mix:gpsAltitude></mix:gpsAltitude>
                            <mix:gpsTimeStamp></mix:gpsTimeStamp>
                            <mix:gpsSatellites></mix:gpsSatellites>
                            <mix:gpsStatus></mix:gpsStatus>
                            <mix:gpsMeasureMode></mix:gpsMeasureMode>
                            <mix:gpsDOP></mix:gpsDOP>
                            <mix:gpsSpeedRef></mix:gpsSpeedRef>
                            <mix:gpsSpeed></mix:gpsSpeed>
                            <mix:gpsTrackRef></mix:gpsTrackRef>
                            <mix:gpsTrack></mix:gpsTrack>
                            <mix:gpsImgDirectionRef></mix:gpsImgDirectionRef>
                            <mix:gpsImgDirection></mix:gpsImgDirection>
                            <mix:gpsMapDatum></mix:gpsMapDatum>
                            <mix:gpsDestLatitudeRef></mix:gpsDestLatitudeRef>
                            {{ GPSDestLatitude gpsGroup element }}
                            <mix:gpsDestLongitudeRef></mix:gpsDestLongitudeRef>
                            {{ GPSDestLongitude gpsGroup element }}
                            <mix:gpsDestBearingRef></mix:gpsDestBearingRef>
                            <mix:gpsDestBearing></mix:gpsDestBearing>
                            <mix:gpsDestDistanceRef></mix:gpsDestDistanceRef>
                            <mix:gpsDestDistance></mix:gpsDestDistance>
                            <mix:gpsProcessingMethod></mix:gpsProcessingMethod>
                            <mix:gpsAreaInformation></mix:gpsAreaInformation>
                            <mix:gpsDateStamp></mix:gpsDateStamp>
                            <mix:gpsDifferential></mix:gpsDifferential>
                        </mix:GPSData>


                        <mix:orientation></mix:orientation>
                        <mix:methodology></mix:methodology>

                    </mix:ImageData>



                </mix:CameraCaptureSettings>
            </mix:DigitalCameraCapture>
        </mix:ImageCaptureMetadata>

    """
    container = _element('ImageCaptureMetadata')
    mix_SourceInformation = _subelement(
        container, 'SourceInformation')
    mix_sourceType = _subelement(mix_SourceInformation, 'sourceType')
    mix_sourceType.text = sourceType

    if SourceID_elements:
        for element in SourceID_elements:
            mix_SourceInformation.append(element)

    mix_SourceSize = _subelement(mix_SourceInformation, 'SourceSize')
    mix_SourceXDimension = _subelement(
        mix_SourceInformation, 'SourceXDimension')
    mix_sourceXDimensionValue = _subelement(mix_SourceXDimension,
                                            'sourceXDimensionValue')
    mix_sourceXDimensionValue.text = sourceXDimensionValue
    mix_sourceXDimensionUnit = _subelement(mix_SourceXDimension,
                                           'sourceXDimensionUnit')
    mix_sourceXDimensionUnit.text = sourceXDimensionUnit

    mix_SourceYDimension = _subelement(
        mix_SourceInformation, 'SourceYDimension')
    mix_sourceYDimensionValue = _subelement(mix_SourceYDimension,
                                            'sourceYDimensionValue')
    mix_sourceYDimensionValue.text = sourceYDimensionValue
    mix_sourceYDimensionUnit = _subelement(mix_SourceYDimension,
                                           'sourceYDimensionUnit')
    mix_sourceYDimensionUnit.text = sourceYDimensionUnit

    mix_SourceZDimension = _subelement(
        mix_SourceInformation, 'SourceZDimension')
    mix_sourceZDimensionValue = _subelement(mix_SourceZDimension,
                                            'sourceZDimensionValue')
    mix_sourceZDimensionValue.text = sourceZDimensionValue
    mix_sourceZDimensionUnit = _subelement(mix_SourceZDimension,
                                           'sourceZDimensionUnit')
    mix_sourceZDimensionUnit.text = sourceZDimensionUnit

    mix_GeneralCaptureInformation = _subelement(container,
                                                'GeneralCaptureInformation')
    mix_dateTimeCreated = _subelement(
        mix_GeneralCaptureInformation, 'dateTimeCreated')
    mix_dateTimeCreated.text = dateTimeCreated

    if imageProducer_elements:
        for element in imageProducer_elements:
            mix_imageProducer = _subelement(mix_GeneralCaptureInformation,
                                            'imageProducer')
            mix_imageProducer.text = element

    mix_captureDevice = _subelement(mix_GeneralCaptureInformation,
                                    'captureDevice')
    mix_captureDevice.text = captureDevice

    mix_ScannerCapture = _subelement(
        container, 'ScannerCapture')
    mix_scannerManufacturer = _subelement(mix_ScannerCapture,
                                          'scannerManufacturer')
    mix_scannerManufacturer.text = scannerManufacturer
    mix_scannerModel = _subelement(mix_ScannerCapture, 'scannerModel')

    mix_scannerModelName = _subelement(mix_scannerModel, 'scannerModelName')
    mix_scannerModelName.text = scannerModelName

    mix_scannerModelNumber = _subelement(
        mix_scannerModel, 'scannerModelNumber')
    mix_scannerModelNumber.text = scannerModelNumber

    mix_scannerModelSerialNo = _subelement(mix_scannerModel,
                                           'scannerModelSerialNo')
    mix_scannerModelSerialNo.text = scannerModelSerialNo

    mix_MaximumOpticalResolution = _subelement(mix_ScannerCapture,
                                               'MaximumOpticalResolution')
    mix_xOpticalResolution = _subelement(
        mix_MaximumOpticalResolution, 'xOpticalResolution')
    mix_xOpticalResolution.text = xOpticalResolution

    mix_yOpticalResolution = _subelement(
        mix_MaximumOpticalResolution, 'yOpticalResolution')
    mix_yOpticalResolution.text = yOpticalResolution

    mix_opticalResolutionUnit = _subelement(mix_MaximumOpticalResolution,
                                            'opticalResolutionUnit')
    mix_opticalResolutionUnit.text = opticalResolutionUnit

    mix_scannerSensor = _subelement(mix_ScannerCapture, 'scannerSensor')
    mix_scannerSensor.text = scannerSensor

    mix_ScanningSystemSoftware = _subelement(mix_ScannerCapture,
                                             'ScanningSystemSoftware')
    mix_scanningSoftwareVersionNo = _subelement(mix_ScannerCapture,
                                                'scanningSoftwareVersionNo')

    mix_DigitalCameraCapture = _subelement(container,
                                           'DigitalCameraCapture')
    mix_digitalCameraManufacturer = _subelement(mix_DigitalCameraCapture,
                                                'digitalCameraManufacturer')
    mix_digitalCameraManufacturer.text = digitalCameraManufacturer

    mix_DigitalCameraModel = _subelement(mix_DigitalCameraCapture,
                                         'DigitalCameraModel')
    mix_digitalCameraModelName = _subelement(mix_DigitalCameraModel,
                                             'DigitalCameraModelName')
    mix_digitalCameraModelName.text = digitalCameraModelName

    mix_digitalCameraModelNumber = _subelement(mix_DigitalCameraModel,
                                               'DigitalCameraModelNumber')
    mix_digitalCameraModelNumber.text = digitalCameraModelNumber

    mix_digitalCameraModelSerialNo = _subelement(mix_DigitalCameraModel,
                                                 'DigitalCameraModelSerialNo')
    mix_digitalCameraModelSerialNo.text = digitalCameraModelSerialNo

    mix_cameraSensor = _subelement(container,
                                   'cameraSensor')
    mix_cameraSensor.text = cameraSensor

    mix_CameraCaptureSettings = _subelement(container,
                                            'CameraCaptureSettings')
    mix_ImageData = _subelement(mix_CameraCaptureSettings,
                                'ImageData')

    mix_fNumber = _subelement(mix_ImageData, 'fNumber')
    mix_fNumber.text = fNumber

    mix_exposureTime = _subelement(mix_ImageData, 'exposureTime')
    mix_exposureTime.text = exposureTime

    if spectralSensitivity_elements:
        for element in spectralSensitivity_elements:
            mix_spectralSensitivity = _subelement(
                mix_ImageData, 'spectralSensitivity')
            mix_spectralSensitivity.text = element

    mix_isoSpeedRatings = _subelement(mix_ImageData, 'isoSpeedRatings')
    mix_isoSpeedRatings.text = isoSpeedRatings

    mix_oECF = _subelement(mix_ImageData, 'oECF')
    mix_oECF.text = oECF

    mix_exifVersion = _subelement(mix_ImageData, 'exifVersion')
    mix_exifVersion.text = exifVersion

    mix_shutterSpeedValue = _subelement(mix_ImageData, 'shutterSpeedValue')
    mix_shutterSpeedValue.text = shutterSpeedValue

    mix_apertureValue = _subelement(mix_ImageData, 'apertureValue')
    mix_apertureValue.text = apertureValue

    mix_brightnessValue = _subelement(mix_ImageData, 'brightnessValue')
    mix_brightnessValue.text = brightnessValue

    mix_exposureBiasValue = _subelement(mix_ImageData, 'exposureBiasValue')
    mix_exposureBiasValue.text = exposureBiasValue

    mix_maxApertureValue = _subelement(mix_ImageData, 'maxApertureValue')
    mix_maxApertureValue.text = maxApertureValue

    mix_SubjectDistance = _subelement(mix_ImageData, 'SubjectDistance')
    mix_distance = _subelement(mix_SubjectDistance, 'distance')
    mix_distance.text = distance

    mix_MinMaxDistance = _subelement(mix_SubjectDistance, 'MinMaxDistance')
    mix_minDistance = _subelement(mix_MinMaxDistance, 'minDistance')
    mix_minDistance.text = minDistance
    mix_maxDistance = _subelement(mix_MinMaxDistance, 'maxDistance')
    mix_maxDistance.text = maxDistance

    mix_meteringMode = _subelement(mix_ImageData, 'meteringMode')
    mix_meteringMode.text = meteringMode

    mix_lightSource = _subelement(mix_ImageData, 'lightSource')
    mix_lightSource.text = lightSource

    mix_flash = _subelement(mix_ImageData, 'flash')
    mix_flash.text = flash

    mix_focalLength = _subelement(mix_ImageData, 'focalLength')
    mix_focalLength.text = focalLength

    mix_flashEnergy = _subelement(mix_ImageData, 'flashEnergy')
    mix_flashEnergy.text = flashEnergy

    mix_backLight = _subelement(mix_ImageData, 'backLight')
    mix_backLight.text = backLight

    mix_exposureIndex = _subelement(mix_ImageData, 'exposureIndex')
    mix_exposureIndex.text = exposureIndex

    mix_sensingMethod = _subelement(mix_ImageData, 'sensingMethod')
    mix_sensingMethod.text = sensingMethod

    mix_cfaPattern = _subelement(mix_ImageData, 'cfaPattern')
    mix_cfaPattern.text = cfaPattern

    mix_autoFocus = _subelement(mix_ImageData, 'autoFocus')
    mix_autoFocus.text = autoFocus

    mix_PrintAspectRatio = _subelement(mix_ImageData, 'PrintAspectRatio')
    mix_xPrintAspectRatio = _subelement(mix_ImageData, 'xPrintAspectRatio')
    mix_xPrintAspectRatio.text = xPrintAspectRatio
    mix_yPrintAspectRatio = _subelement(mix_ImageData, 'yPrintAspectRatio')
    mix_yPrintAspectRatio.text = yPrintAspectRatio

    mix_GPSData = _element('GPSData')
    mix_gpsVersionID = _subelement(mix_GPSData, 'gpsVersionID')
    mix_gpsVersionID.text = gpsVersionID

    mix_gpsLatitudeRef = _subelement(mix_GPSData, 'gpsLatitudeRef')
    mix_gpsLatitudeRef.text = gpsLatitudeRef

    if GPSLatitude_element:
        mix_GPSData.append(GPSLatitude_element)

    mix_gpsLongitudeRef = _subelement(mix_GPSData, 'gpsLongitudeRef')
    mix_gpsLongitudeRef.text = gpsLongitudeRef

    if GPSLongitude_element:
        mix_GPSData.append(GPSLongitude_element)

    mix_gpsAltitudeRef = _subelement(mix_GPSData, 'gpsAltitudeRef')
    mix_gpsAltitudeRef.text = gpsAltitudeRef

    mix_gpsAltitude = _subelement(mix_GPSData, 'gpsAltitude')
    mix_gpsAltitude.text = gpsAltitude

    mix_gpsTimeStamp = _subelement(mix_GPSData, 'gpsTimeStamp')
    mix_gpsTimeStamp.text = gpsTimeStamp

    mix_gpsSatellites = _subelement(mix_GPSData, 'gpsSatellites')
    mix_gpsSatellites.text = gpsSatellites

    mix_gpsStatus = _subelement(mix_GPSData, 'gpsStatus')
    mix_gpsStatus.text = gpsStatus

    mix_gpsMeasureMode = _subelement(mix_GPSData, 'gpsMeasureMode')
    mix_gpsMeasureMode.text = gpsMeasureMode

    mix_gpsDOP = _subelement(mix_GPSData, 'gpsDOP')
    mix_gpsDOP.text = gpsDOP

    mix_gpsSpeedRef = _subelement(mix_GPSData, 'gpsSpeedRef')
    mix_gpsSpeedRef.text = gpsSpeedRef

    mix_gpsSpeed = _subelement(mix_GPSData, 'gpsSpeed')
    mix_gpsSpeed.text = gpsSpeed

    mix_gpsTrackRef = _subelement(mix_GPSData, 'gpsTrackRef')
    mix_gpsTrackRef.text = gpsTrackRef

    mix_gpsTrack = _subelement(mix_GPSData, 'gpsTrack')
    mix_gpsTrack.text = gpsTrack

    mix_gpsImgDirectionRef = _subelement(mix_GPSData, 'gpsImgDirectionRef')
    mix_gpsImgDirectionRef.text = gpsImgDirectionRef

    mix_gpsImgDirection = _subelement(mix_GPSData, 'gpsImgDirection')
    mix_gpsImgDirection.text = gpsImgDirection

    mix_gpsMapDatum = _subelement(mix_GPSData, 'gpsMapDatum')
    mix_gpsMapDatum.text = gpsMapDatum

    mix_gpsDestLatitudeRef = _subelement(mix_GPSData, 'gpsDestLatitudeRef')
    mix_gpsDestLatitudeRef.text = gpsDestLatitudeRef

    if GPSDestLatitude_element:
        mix_GPSData.append(GPSDestLatitude_element)

    mix_gpsDestLongitudeRef = _subelement(mix_GPSData, 'gpsDestLongitudeRef')
    mix_gpsDestLongitudeRef.text = gpsDestLongitudeRef

    if gpsDestLongitude_element:
        mix_GPSData.append(gpsDestLongitude_element)

    mix_gpsDestBearingRef = _subelement(mix_GPSData, 'gpsDestBearingRef')
    mix_gpsDestBearingRef.text = gpsDestBearingRef

    mix_gpsDestBearing = _subelement(mix_GPSData, 'gpsDestBearing')
    mix_gpsDestBearing.text = gpsDestBearing

    mix_gpsDestDistanceRef = _subelement(mix_GPSData, 'gpsDestDistanceRef')
    mix_gpsDestDistanceRef.text = gpsDestDistanceRef

    mix_gpsDestDistance = _subelement(mix_GPSData, 'gpsDestDistance')
    mix_gpsDestDistance.text = gpsDestDistance

    mix_gpsProcessingMethod = _subelement(mix_GPSData, 'gpsProcessingMethod')
    mix_gpsProcessingMethod.text = gpsProcessingMethod

    mix_gpsAreaInformation = _subelement(mix_GPSData, 'gpsAreaInformation')
    mix_gpsAreaInformation.text = gpsAreaInformation

    mix_gpsDateStamp = _subelement(mix_GPSData, 'gpsDateStamp')
    mix_gpsDateStamp.text = gpsDateStamp

    mix_gpsDifferential = _subelement(mix_GPSData, 'gpsDifferential')
    mix_gpsDifferential.text = gpsDifferential

    mix_orientation = _subelement(mix_ImageData, 'orientation')
    mix_orientation.text = orientation

    mix_methodology = _subelement(mix_ImageData, 'methodology')
    mix_methodology.text = methodology

    return container


def mix_SourceID(sourceIDType=None, sourceIDValue=None):
    """Returns MIX sourceID element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:sourceID>
            <mix:sourceIDType></mix:sourceIDType>
            <mix:sourceIDValue></mix:sourceIDValue>
        </mix:sourceID>

    """
    mix_sourceID = _element('sourceID')
    mix_sourceIDType = _subelement(mix_sourceID, 'sourceIDType')
    mix_sourceIDType.text = sourceIDType

    mix_sourceIDValue = _subelement(mix_sourceID, 'sourceIDValue')
    mix_sourceIDValue.text = sourceIDValue

    return mix_sourceID


def mix_gpsGroup(degrees=None, minutes=None, seconds=None):
    """Returns MIX gpsGroup element

    :Schema documentation: Data Dictionary - Technical Metadata for Digital Still Images (ANSI/NISO Z39.87-2006)

    Returns the following ElementTree structure::

        <mix:gpsGroup>
            <mix:degrees></mix:degrees>
            <mix:minutes></mix:minutes>
            <mix:seconds></mix:seconds>
        </mix:sourceID>

    """
    elem = _element('gpsGroup')
    mix_degrees = _subelement(elem, 'degrees')
    mix_degrees.text = degrees

    mix_minutes = _subelement(elem, 'minutes')
    mix_minutes.text = minutes

    mix_seconds = _subelement(elem, 'seconds')
    mix_seconds.text = seconds

    return elem
