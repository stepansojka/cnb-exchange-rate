
from six.moves.urllib.request import urlopen

import datetime
import csv
import sys

host = 'www.cnb.cz'

URL = 'http://%s/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/prumerne_mena.txt?mena=%s'
DAILY_URL = 'http://%s/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/vybrane.txt?mena=%s&od=%s&do=%s'
MONTHLY_AVERAGE_TABLE_IDX = 0
CUMULATIVE_MONTHLY_AVERAGE_TABLE_IDX = 1
QUARTERLY_AVERAGE_TABLE_IDX = 2
FIELD_DELIMITER = '|'
TABLE_DELIMITER = '\n\n'
TABLE_ENCODING = 'UTF-8'

def set_host(h):
    global host
    host = h

def download(url):
    stream = urlopen(url)
    raw = stream.read()

    return raw.decode('ascii', 'ignore')

def parse_table(table):
    csv_reader = csv.reader(table.split('\n'), delimiter=FIELD_DELIMITER)
    d = {}

    for row in csv_reader:
        if len(row) > 1:
            d[row[0]] = row[1:]
            
    return d

def averages(currency, table_index):
    url = URL % (host, currency)
    tables = download(url).split(TABLE_DELIMITER)
    return parse_table(tables[table_index])

def rate(t, key, index):
    s = t[str(key)][index]
    return float(s.replace(',','.'))

def monthly_average(currency, year, month):
    try:
        t = averages(currency, MONTHLY_AVERAGE_TABLE_IDX)
        return rate(t, year, month - 1)
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, month %s not found' % (currency, year, month))


def cumulative_monthly_average(currency, year, month):
    try:
        t = averages(currency, CUMULATIVE_MONTHLY_AVERAGE_TABLE_IDX)
        return rate(t, year, month - 1)
    except (ValueError, KeyError, IndexError):
        raise ValueError('cumulative average rate for %s, year %s, month %s not found' % (currency, year, month))


def quarterly_average(currency, year, quarter):
    try:
        t = averages(currency, QUARTERLY_AVERAGE_TABLE_IDX)
        return rate(t, year, quarter - 1)
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, quarter %s not found' % (currency, year, quarter))

def daily_rate(currency, date):
    try:
        date_str = date.strftime('%d.%m.%Y')
        url = DAILY_URL % (host, currency, date_str, date_str)
        t = parse_table(download(url))
        return rate(t, date_str, 0)
    except (ValueError, KeyError, IndexError):
        raise ValueError('rate for %s at %s not found' % (currency, date))
    

if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = int(sys.argv[3])

    print(quarterly_average(currency, year, quarter))

