import pytest

import cnb_exchange_rate as cnb

def test_quarter():
    assert 27.447 == cnb.quarter_average('EUR', 2014, 2)
    assert 27.618 == cnb.quarter_average('EUR', 2014, 3)
    assert 34.798 == cnb.quarter_average('EUR', 2001, 1)

def test_quarter_with_unexpected_year():
    with pytest.raises(ValueError) as e:
        cnb.quarter_average('EUR', 1492, 1)

    assert 'year 1492 not found' in str(e.value)

def test_quarter_with_unexpected_quarter():
    with pytest.raises(ValueError) as e:
        cnb.quarter_average('EUR', 2010, 42)

    assert 'quarter 42 not found' in str(e.value)

def test_quarter_with_invalid_currency():
    with pytest.raises(ValueError) as e:
        cnb.quarter_average('WTF', 2009, 2)

    assert 'currency WTF not found' in str(e.value)
