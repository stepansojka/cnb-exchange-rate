
from six.moves.urllib.request import urlopen

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


def download_average_rate_table(currency, table_index):
    url = URL % (host, currency)
    tables = download(url).split(TABLE_DELIMITER)
    return tables[table_index]

def average_rates_table(currency, table_index):
    raw_table = download_average_rate_table(currency, table_index)
    return parse_table(raw_table)

def rate_string_to_float(s):
    return float(s.replace(',','.'))

def monthly_average(currency, year, month):
    try:
        rate_table = average_rates_table(currency, MONTHLY_AVERAGE_TABLE_IDX)
        return rate_string_to_float(rate_table[str(year)][month - 1])
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, month %s not found' % (currency, year, month))


def cumulative_monthly_average(currency, year, month):
    try:
        rate_table = average_rates_table(currency, CUMULATIVE_MONTHLY_AVERAGE_TABLE_IDX)
        return rate_string_to_float(rate_table[str(year)][month - 1])
    except (ValueError, KeyError, IndexError):
        raise ValueError('cumulative average rate for %s, year %s, month %s not found' % (currency, year, month))


def quarterly_average(currency, year, quarter):
    try:
        rate_table = average_rates_table(currency, QUARTERLY_AVERAGE_TABLE_IDX)
        return rate_string_to_float(rate_table[str(year)][quarter - 1]) 
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, quarter %s not found' % (currency, year, quarter))

def daily_rate(currency, date):
    date_str = date.strftime('%d.%m.%Y')
    url = DAILY_URL % (host, currency, date_str, date_str)
    
    table = parse_table(download(url))

    rate_str = table[date_str][0]
    return rate_string_to_float(rate_str)
    

if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = int(sys.argv[3])

    print(quarterly_average(currency, year, quarter))

