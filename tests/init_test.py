"""Tests the init module."""
from __future__ import unicode_literals

import nisomix


def test_import():
    """Tests import."""
    nisomix.fixity(algorithm='MD5', digest='test')
