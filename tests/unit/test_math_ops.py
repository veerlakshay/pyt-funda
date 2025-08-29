# AAA style: Arrange, Act, Assert
from pickletools import pyset

import pytest
from app.math_ops import add, divide

def test_add_two_positive_numbers():
    # Arrange
    a, b = 2, 3

    # Act
    result = add(a, b)

    # Assert
    assert result == 5

def test_divide_simple():
    assert divide(10, 2) == 5

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError) as e:
        divide(10,0)
        #optional: assert message
        assert "division by zero" in str(e.value).lower()

@pytest.mark.parametrize(
    "a, b, expected",[
        (1,2,3),
        (-1,1,0),
        (1.5,2.5,4.0),
    ],
    ids=["positive", "mixed-to-zero", "float"]
)
def test_add_various(a, b, expected):
    assert add(a,b) == expected

@pytest.mark.parametrize(
    "a , b",
    [
        (1, 0),
        (-5,0),
        (0,0),
    ],
    ids=["pos/zero", "neg/zero", "zero/zero"]
)
def test_divide_raises_for_zero(a, b):
    with pytest.raises(ZeroDivisionError):
        divide(a , b)

@pytest.mark.parametrize(
    "a,b,expected",[
        (10, 4, 2.5),
        (1, 3,  0.3333333333333333),
    ],
    ids=["even", "reciprocal"]
)
def test_divide_floats(a , b , expected):
    assert divide(a, b) == pytest.approx(expected, rel=1e-12)

@pytest.mark.parametrize(
    "a, b, expected",[
        (1, 1, 1),
        (2, 3, 6),
        (500, 0, 0),
    ],
    ids=["1cross1", "2cross3", "500cross0"]
)
def test_mul(a, b, expected):
    assert a * b == expected

