import rshanker779_common as utils
import pytest


@pytest.fixture
def A():
    class A(utils.StringMixin, utils.EqualsMixin, utils.JSONMixin):
        a = 1

        def __init__(self, b):
            self.b = b
            self.d = "a"
            self.e = [1, 2, 3]

        def c(self):
            return 3

    return A
