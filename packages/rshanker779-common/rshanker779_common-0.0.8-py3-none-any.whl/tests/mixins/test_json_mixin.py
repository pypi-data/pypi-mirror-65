import json

import rshanker779_common as utils


class InnerNested(utils.JSONMixin):
    def __init__(self):
        self.a = 1


class B(utils.JSONMixin):
    def __init__(self):
        self.a = InnerNested()
        self.b = (1, 2, 3)


def test_json_mixin(A):
    res = json.loads(A(3).to_json())
    assert res == {"b": 3, "d": "a", "e": [1, 2, 3]}


def test_nested_classes():
    res = json.loads(B().to_json())
    assert res == {"b": [1, 2, 3], "a": {"InnerNested": {"a": 1}}}
