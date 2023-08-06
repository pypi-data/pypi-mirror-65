import doctest


def test_suite():
    """Test doctest as unittest."""
    # This should help with https://github.com/pytest-dev/pytest/issues/1862
    return doctest.DocFileSuite('../../../../README.rst')
