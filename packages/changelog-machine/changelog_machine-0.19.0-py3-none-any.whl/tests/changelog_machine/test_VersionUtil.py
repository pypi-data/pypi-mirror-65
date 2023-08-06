import pytest

from changelog_machine.versions.VersionUtil import VersionNumber


class TestVersionNumber:
    testdata = [
        ("", "1.1.1"),
        ("1.1", "1.1.1"),
        ("1.1.1", "1.2.1"),
        ("1.1.1", "1.20.1"),
        ("1.1.1", "1.1rc.1"),
    ]

    @pytest.mark.parametrize("v1, v2", testdata)
    def test_lt(self, v1, v2):
        assert VersionNumber(v1).__lt__(VersionNumber(v2))
        assert not VersionNumber(v2).__lt__(VersionNumber(v1))

    def test_lt_when_equal(self):
        assert not VersionNumber("1.1.1").__lt__(VersionNumber("1.1.1"))
