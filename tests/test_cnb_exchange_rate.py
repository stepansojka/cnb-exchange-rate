import pytest

import cnb_exchange_rate as cnb

import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class FakeCNBHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            p = '/home/stepan/cnb-exchange-rate/tests/data/' + self.path
            print(p)
            f = open(p)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

@pytest.fixture(scope='module')
def fake_server(request):
    cnb.set_host('127.0.0.1:8080')
    server = HTTPServer(('127.0.0.1', 8080), FakeCNBHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    def fin():
        server.shutdown()

    request.addfinalizer(fin)

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

