
from six.moves.urllib.request import urlopen

import csv
import sys

host = 'www.cnb.cz'

URL = 'http://%s/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/prumerne_mena.txt?mena=%s'
MONTHLY_AVERAGE_TABLE_IDX = 0
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
    
    tables = str(raw, encoding=TABLE_ENCODING).split(TABLE_DELIMITER)
    return tables[table_index]

def average_rates(currency, table_index):
    raw_table = download_average_rate_table(currency, table_index)
    csv_reader = csv.reader(raw_table.split('\n'), delimiter=FIELD_DELIMITER)
    rate_table = {}

    for row in csv_reader:
        if len(row) > 1:
            try:
                year = int(row[0])
                rates = [ float(r.replace(',','.')) for r in row[1:] if len(r) > 0 ]
                rate_table[year] = rates
            except ValueError:
                pass

    return rate_table

def quarterly_average(currency, year, quarter):
    rate_table = average_rates(currency, QUARTERLY_AVERAGE_TABLE_IDX)

    try:
        return rate_table[year][quarter - 1]
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, quarter %s not found' % (currency, year, quarter))

def monthly_average(currency, year, month):
    rate_table = average_rates(currency, MONTHLY_AVERAGE_TABLE_IDX)

    try:
        return rate_table[year][month - 1]
    except (ValueError, KeyError, IndexError):
        raise ValueError('average rate for %s, year %s, month %s not found' % (currency, year, month))

if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = int(sys.argv[3])

    print(quarter_average(currency, year, quarter))

