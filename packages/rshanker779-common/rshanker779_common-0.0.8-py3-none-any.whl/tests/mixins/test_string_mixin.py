def test_string_mixin(A):
    assert str(A(2)) == "<A>(b=2, d=a, e=[1, 2, 3])"
    assert str(A(4)) == repr(A(4))
