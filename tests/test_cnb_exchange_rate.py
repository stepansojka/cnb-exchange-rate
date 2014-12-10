import pytest

import cnb_exchange_rate as cnb

def test_quarterly_with_existing_EUR():
    assert 27.447 == cnb.quarterly_average('EUR', 2014, 2)

def test_quarterly_with_existing_USD():
    assert 20.845 == cnb.quarterly_average('USD', 2014, 3)

def test_quarterly_with_year_with_no_data():
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('SGD', 2001, 1)

    assert 'not found' in str(e.value)

def test_quarterly_with_unexpected_year():
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('EUR', 1492, 1)

    assert 'not found' in str(e.value)

def test_quarterly_with_unexpected_quarter():
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('EUR', 2010, 42)

    assert 'not found' in str(e.value)

def test_quarterly_with_invalid_currency():
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('WTF', 2009, 2)

    assert 'not found' in str(e.value)

def test_monthly_with_existing_SGD():
    assert 13.114 == cnb.monthly_average('SGD', 2010, 1)

