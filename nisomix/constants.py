# encoding=utf8
"""Global variables for nisomix."""


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

IMAGE_DATA_CONTENTS = {'fnumber': None,
                       'exposure_time': None,
                       'exposure_program': None,
                       'spectral_sensitivity': None,
                       'isospeed_ratings': None,
                       'oecf': None,
                       'exif_version': None,
                       'shutter_speed_value': None,
                       'aperture_value': None,
                       'brightness_value': None,
                       'exposure_bias_value': None,
                       'max_aperture_value': None,
                       'distance': None,
                       'min_distance': None,
                       'max_distance': None,
                       'metering_mode': None,
                       'light_source': None,
                       'flash': None,
                       'focal_length': None,
                       'flash_energy': None,
                       'back_light': None,
                       'exposure_index': None,
                       'sensing_method': None,
                       'cfa_pattern': None,
                       'auto_focus': None,
                       'x_print_aspect_ratio': None,
                       'y_print_aspect_ratio': None}

GPS_DATA_CONTENTS = {'version_id': None,
                     'lat_ref': None,
                     'lat_degrees': None,
                     'lat_minutes': None,
                     'lat_seconds': None,
                     'long_ref': None,
                     'long_degrees': None,
                     'long_minutes': None,
                     'long_seconds': None,
                     'altitude_ref': None,
                     'altitude': None,
                     'timestamp': None,
                     'satellites': None,
                     'status': None,
                     'measure_mode': None,
                     'dop': None,
                     'speed_ref': None,
                     'speed': None,
                     'track_ref': None,
                     'track': None,
                     'img_direction_ref': None,
                     'direction': None,
                     'map_datum': None,
                     'dest_lat_ref': None,
                     'dest_lat_degrees': None,
                     'dest_lat_minutes': None,
                     'dest_lat_seconds': None,
                     'dest_long_ref': None,
                     'dest_long_degrees': None,
                     'dest_long_minutes': None,
                     'dest_long_seconds': None,
                     'dest_bearing_ref': None,
                     'dest_bearing': None,
                     'dest_distance_ref': None,
                     'dest_distance': None,
                     'processing_method': None,
                     'area_information': None,
                     'datestamp': None,
                     'differential': None,
                     'gps_groups': None}
