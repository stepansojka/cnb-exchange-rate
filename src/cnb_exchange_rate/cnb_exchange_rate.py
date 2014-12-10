
from six.moves.urllib.request import urlopen

import csv
import sys

URL = 'http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/prumerne_mena.txt?mena=%s'
MONTHLY_AVERAGE_TABLE_IDX = 0
QUARTERLY_AVERAGE_TABLE_IDX = 2
FIELD_DELIMITER = '|'
TABLE_DELIMITER = '\n\n'
TABLE_ENCODING = 'UTF-8'

def average_rates(currency, table_index):
    stream = urlopen(URL % currency)
    raw = stream.read().decode(TABLE_ENCODING)
    if len(raw) < 16:
        raise ValueError('currency %s not found' % currency)
    
    tables = raw.split(TABLE_DELIMITER)
    csv_reader = csv.reader(tables[table_index].split('\n'), delimiter=FIELD_DELIMITER)

    rate_table = {}
    for row in csv_reader:
        if len(row) > 1:
            try:
                y = int(row[0])
                rates = [ float(r.replace(',','.')) for r in row[1:] if len(r) > 0 ]
                rate_table[y] = rates
            except ValueError:
                pass

    return rate_table

def quarter_average(currency, year, quarter):
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
        raise ValueError('average rate for %s, year %s, month %s not found' % (currency, year, quarter))


if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = int(sys.argv[3])

    print(quarter_average(currency, year, quarter))

