import pytest


class TestGrouping:
    def test_from_group(self):
        print("Hello from group")
        assert (True)


def raises_exc(self):
    raise Exception("Hello")


class TestAnotherGroup:
    def test_tests(self):
        print("Hello from tests")
        assert (True)

    def test_raising(self):
        with pytest.raises(Exception):
            raise Exception()
