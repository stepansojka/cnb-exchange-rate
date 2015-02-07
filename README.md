CNB Exchange Rate
================
[![Build Status](https://travis-ci.org/stepansojka/cnb-exchange-rate.svg)](https://travis-ci.org/stepansojka/cnb-exchange-rate)
[![Supported Python Versions](https://pypip.in/py_versions/cnb-exchange-rate/badge.svg)](https://pypi.python.org/pypi/cnb-exchange-rate/)
[![Latest Version](https://pypip.in/version/cnb-exchange-rate/badge.svg)](https://pypi.python.org/pypi/cnb-exchange-rate/)

Python lib that downloads exchange rates from the Czech National Bank. 
Released under MIT License (see the LICENSE file).

### Installation

If you have downloaded the source code:

    python setup.py install

or if you want to obtain a copy from the Pypi repository:

    pip install cnb-exchange-rate

Both commands will install the required package dependencies. The code is available on GitHub, which can be browsed at [github](https://github.com/stepansojka/cnb-exhchange-rate) or cloned by running

    git clone git://github.com/stepansojka/cnb-exchange-rate
    
### Usage
To import import the library:

    >>> import cnb_exchange_rate
    
The rates can be obtained be obtained using:

    >>> import datetime
    >>> cnb_exchange_rate.daily_rate('EUR', datetime.date(2015, 1, 20))
    27.845

    >>> cnb_exchange_rate.monthly_average('EUR', 2015, 1)
    27.895
    
    >>> cnb_exchange_rate.quarterly_average('EUR', 2014, 4)
    27.624

### Running Tests

The easiest way to run test is by using [tox](https://pypi.python.org/pypi/tox), a wrapper around virtualenv. It will take care of setting up environnements with the proper dependencies installed and execute test commands. To install it simply:

    pip install tox

Then run:

    tox
