import pytest
from .utils import dict_inject

def test_dict_inject():
    # Simple case
    assert dict_inject({'x': 1}, {'y': 2}) == {'x': 1, 'y': 2}

    # Recursive case
    assert dict_inject({'foo': {'x': 1}}, {'foo': {'y': 2}}) == {'foo': {'x': 1, 'y': 2}}

    # Same value case
    assert dict_inject({'foo': {'x': 1}}, {'foo': {'x': 1}}) == {'foo': {'x': 1}}

    # Different value case
    with pytest.raises(Exception, match=r"Conflicting values for foo.x: current value is '1', trying to update to '2'"):
        dict_inject({'foo': {'x': 1}}, {'foo': {'x': 2}})
