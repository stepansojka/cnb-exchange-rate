import pytest

import cnb_exchange_rate as cnb

def test_quarter_with_existing_EUR():
    assert 27.447 == cnb.quarter_average('EUR', 2014, 2)

def test_quarter_with_existing_USD():
    assert 20.845 == cnb.quarter_average('USD', 2014, 3)

def test_quarter_with_year_with_no_data():
    with pytest.raises(ValueError) as e:
        cnb.quarter_average('SGD', 2001, 1)

    assert 'year 2001 not found' in str(e.value)

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
