"""Import everything for making convenient use of the library possible"""
__version__ = '0.16'

# flake8 doesn't like these imports, but they are needed for other repos
# flake8: noqa
from nisomix.base import *
from nisomix.object_information_base import *
from nisomix.image_information_base import *
from nisomix.capture_metadata_base import *
from nisomix.assessment_metadata_base import *
from nisomix.change_history_base import *
from nisomix.constants import *
