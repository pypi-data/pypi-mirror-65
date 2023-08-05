import pytest

import bwgds.bwgcalc as calc


def test_squares():
    a,b = calc.squares(4,10)
    assert a == 16
    assert b == 100

def test_add():
    a = calc.add(1,2)
    assert a == 3
    
def test_sub():
    a = calc.sub(10,2)
    assert a == 8
    

def test_square():
    a = calc.square(7)
    assert a == 49


