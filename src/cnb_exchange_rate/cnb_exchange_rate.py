
from six.moves.urllib.request import urlopen

import csv
import sys

host = 'www.cnb.cz'

URL = 'http://%s/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/prumerne_mena.txt?mena=%s'
DAILY_URL = 'http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/vybrane.txt?mena=SGD&od=02.01.2014&do=02.01.2014'
MONTHLY_AVERAGE_TABLE_IDX = 0
CUMULATIVE_MONTHLY_AVERAGE_TABLE_IDX = 1
QUARTERLY_AVERAGE_TABLE_IDX = 2
FIELD_DELIMITER = '|'
TABLE_DELIMITER = '\n\n'
TABLE_ENCODING = 'UTF-8'

def set_host(h):
    global host
    host = h

def download_average_rate_table(currency, table_index):
    stream = urlopen(URL % (host, currency))
    raw = stream.read()

    if len(raw) < 16:
        raise ValueError('currency %s not found' % currency)
    
    tables = raw.decode('ascii', 'ignore').split(TABLE_DELIMITER)
    return tables[table_index]

def average_rates(currency, table_index):
    raw_table = download_average_rate_table(currency, table_index)
    csv_reader = csv.reader(raw_table.split('\n'), delimiter=FIELD_DELIMITER)
    rate_table = {}

    for row in csv_reader:
        if len(row) > 1:
            try:
                rate_table[row[0]] = row[1:]
            except ValueError:
                pass

    return rate_table

def rate_string_to_float(s):
    return float(s.replace(',','.'))

def monthly_average(currency, year, month):
    rate_table = average_rates(currency, MONTHLY_AVERAGE_TABLE_IDX)

    try:
        return rate_string_to_float(rate_table[str(year)][month - 1])
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, month %s not found' % (currency, year, month))


def cumulative_monthly_average(currency, year, month):
    rate_table = average_rates(currency, CUMULATIVE_MONTHLY_AVERAGE_TABLE_IDX)

    try:
        return rate_string_to_float(rate_table[str(year)][month - 1])
    except (ValueError, KeyError, IndexError):
        raise ValueError('cumulative average rate for %s, year %s, month %s not found' % (currency, year, month))


def quarterly_average(currency, year, quarter):
    rate_table = average_rates(currency, QUARTERLY_AVERAGE_TABLE_IDX)

    try:
        return rate_string_to_float(rate_table[str(year)][quarter - 1]) 
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, quarter %s not found' % (currency, year, quarter))

def daily_rate(currency, date):
    date_str = date.strftime('%d.%m.%Y')
    stream = urlopen(DAILY_URL)
    raw = stream.read()
    
    table = raw.decode('ascii', 'ignore')

    csv_reader = csv.reader(table.split('\n'), delimiter=FIELD_DELIMITER)
    rate_table = {}

    for row in csv_reader:
        if len(row) > 1:
            try:
                rate_table[row[0]] = row[1:]
            except ValueError:
                pass

    rate_str = rate_table[date_str][0]
    return rate_string_to_float(rate_str)
    

if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = int(sys.argv[3])

    print(quarterly_average(currency, year, quarter))

