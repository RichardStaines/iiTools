from Utils.TimeUtils import TimeUtils
import datetime
import pytest
from Utils.Log import Log


@pytest.fixture(scope="module")
def setup():
    Log.create("Test.log", "INFO,L1,L2,L3")


@pytest.mark.parametrize("in_date,expected",[
    ('19/10/2023', True),
    ('19/10/2022', False),
    ('19/10/2019', False),
])
def test_is_this_year(setup, in_date, expected):
    dt = datetime.datetime.strptime(in_date, '%d/%m/%Y')
    res = TimeUtils.is_this_year(dt)
    assert res == expected


@pytest.mark.parametrize("in_date,expected",[
    ('19/10/2023', False),
    ('19/10/2022', True),
    ('19/10/2019', False),
])
def test_is_last_year(setup, in_date, expected):
    dt = datetime.datetime.strptime(in_date, '%d/%m/%Y')
    res = TimeUtils.is_last_year(dt)
    assert res == expected
