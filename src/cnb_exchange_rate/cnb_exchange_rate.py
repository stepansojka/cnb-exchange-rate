from six.moves.urllib.request import urlopen
import sys

URL = 'http://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/prumerne_mena.txt?mena=%s'
DELIMITER = '|'

def quarter_average(currency, year, quarter):
    f = urlopen(URL % currency)
    all_rates = f.read().decode('UTF-8')
    if len(all_rates) < 16:
        raise ValueError('currency %s not found' % currency)

    try:
        line_start = all_rates.rindex(str(year) + DELIMITER)
        line_end = all_rates.index('\n', line_start)
        line = all_rates[line_start:line_end]
    except ValueError:
        raise ValueError('year %s not found' % year)

    try:
        rate_str = line.split(DELIMITER)[quarter]
    except IndexError:
        raise ValueError('quarter %s not found' % quarter)
    
    rate = float(rate_str.replace(',', '.'))
    return rate

if __name__ == '__main__':
    currency = sys.argv[1]
    year = sys.argv[2]
    quarter = sys.argv[3]

    print(quarter_average(currency, year, quarter))

