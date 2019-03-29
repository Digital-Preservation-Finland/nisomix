"""Utility functions and global variables."""

from xml_helpers.utils import XSI_NS


MIX_NS = 'http://www.loc.gov/mix/v20'

NAMESPACES = {'mix': MIX_NS,
              'xsi': XSI_NS}


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
