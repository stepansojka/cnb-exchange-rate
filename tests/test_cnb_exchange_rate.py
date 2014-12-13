import cnb_exchange_rate as cnb
import pytest
import fake_cnb_server
import datetime

@pytest.fixture(scope='module')
def fake_server(request):
    cnb.set_host('127.0.0.1:8080')
    server = fake_cnb_server.start()

    def fin():
        server.shutdown()

    request.addfinalizer(fin)

def test_monthly_with_existing_SGD(fake_server):
    assert 13.114 == cnb.monthly_average('SGD', 2010, 1)

def test_monthly_with_existing_AUD(fake_server):
    assert 15.736 == cnb.monthly_average('AUD', 2007, 12)

def test_monthly_with_invalid_currency(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.monthly_average('WTF', 2009, 2)

    assert 'not found' in str(e.value)

def test_montly_with_year_with_no_data(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.monthly_average('EUR', 1991, 1)

    assert 'not found' in str(e.value)

def test_monthly_with_unexpected_year(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.monthly_average('EUR', 1492, 1)

    assert 'not found' in str(e.value)

def test_monthly_with_invalid_month(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.monthly_average('EUR', 2010, 42)

    assert 'not found' in str(e.value)

def test_cumulative_monthly_with_existing_SGD(fake_server):
    assert 13.114 == cnb.cumulative_monthly_average('SGD', 2010, 1)

def test_cumulative_monthly_with_existing_AUD(fake_server):
    assert 16.988 == cnb.cumulative_monthly_average('AUD', 2007, 12)

def test_cumulative_monthly_with_invalid_currency(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.cumulative_monthly_average('WTF', 2009, 2)

    assert 'not found' in str(e.value)

def test_cumulative_montly_with_year_with_no_data(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.cumulative_monthly_average('EUR', 1991, 1)

    assert 'not found' in str(e.value)

def test_cumulative_monthly_with_unexpected_year(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.cumulative_monthly_average('EUR', 1492, 1)

    assert 'not found' in str(e.value)

def test_cumulative_monthly_with_invalid_month(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.cumulative_monthly_average('EUR', 2010, 42)

    assert 'not found' in str(e.value)

def test_quarterly_with_existing_EUR(fake_server):
    assert 27.447 == cnb.quarterly_average('EUR', 2014, 2)

def test_quarterly_with_existing_USD(fake_server):
    assert 20.845 == cnb.quarterly_average('USD', 2014, 3)

def test_quarterly_with_year_with_no_data(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('SGD', 2001, 1)

    assert 'not found' in str(e.value)

def test_quarterly_with_unexpected_year(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('EUR', 1492, 1)

    assert 'not found' in str(e.value)

def test_quarterly_with_unexpected_quarter(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('EUR', 2010, 42)

    assert 'not found' in str(e.value)

def test_quarterly_with_invalid_currency(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.quarterly_average('WTF', 2009, 2)

    assert 'not found' in str(e.value)

def test_daily_SGD_at_02012014(fake_server):
    assert 15.859 == cnb.daily_rate('SGD', datetime.date(2014, 1, 2))

def test_daily_EUR_at_22112011(fake_server):
    assert 25.485 == cnb.daily_rate('EUR', datetime.date(2011, 11, 22))

def test_daily_with_year_with_no_data(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.daily_rate('SGD', datetime.datetime(2001, 1, 1))

    assert 'not found' in str(e.value)

def test_daily_with_invalid_currency(fake_server):
    with pytest.raises(ValueError) as e:
        cnb.daily_rate('XYZ', datetime.datetime(2011, 1, 1))

    assert 'not found' in str(e.value)
