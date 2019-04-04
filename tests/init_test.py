"""Tests the init module."""
import nisomix


def test_import():
    """Tests import."""
    fix = nisomix.fixity(algorithm='MD5', digest='test')
