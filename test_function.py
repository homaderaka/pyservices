
def function(a):
    return a


def test_function():
    a = True
    assert a == function(a)
    assert a != function(not a)
