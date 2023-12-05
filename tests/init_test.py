"""Tests the init module."""

import nisomix


def test_import():
    """Tests import."""
    nisomix.fixity(algorithm='MD5', digest='test')
