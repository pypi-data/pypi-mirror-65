class B:
    pass


def test_eq(A):
    assert not A(1) == B()
    assert not A(3) == A(5)
    assert A(7) == A(7)


def test_hash(A):
    assert hash(A(4)) == hash(A(4))
    assert hash(A({"a": "b"})) == hash(A({"a": "b"}))
    assert not hash(A(3)) == hash(A(4))
