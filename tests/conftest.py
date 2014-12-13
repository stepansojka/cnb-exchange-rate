import pytest

import fake_cnb_server

def pytest_addoption(parser):
    parser.addoption('--fake', action='store_true', help='use fake CNB server')

@pytest.fixture(scope='module')
def fake_server(request):
    if request.config.getoption('--fake', default=False):
        server = fake_cnb_server.start()

        def fin():
            server.shutdown()

        request.addfinalizer(fin)
