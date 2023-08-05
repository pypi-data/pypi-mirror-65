import pytest

import bwgds.bwggreeting as frz

def test_hi():
    s = frz.hi()
    assert isinstance(s, str)