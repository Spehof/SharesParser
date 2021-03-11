import requests
import argparse
import validators
import sys
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class b_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def validate_finviz_url(url):
    parsed_uri = urlparse(url)
    if parsed_uri.hostname == 'finviz.com':
        return True
    else:
        return False


def get_commandline_args():
    parser = argparse.ArgumentParser(description='This script parse shares tickers from finviz.com')

    parser.add_argument('-c', '--cheap',
                        help='Parse only cheap shares (Under 10$)',
                        action='store_true')
    parser.add_argument('-e', '--expensive',
                        help='Parse only expensive shares (Over 10$)',
                        action='store_true')
    parser.add_argument('-l', '--link',
                        help='Create custom link with custom params and get here')
    args = parser.parse_args()
    return args


def get_page_html(url, params=None):
    page_html = requests.get(url, headers=HEADERS, params=params)
    return page_html


def get_paging_count(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    tags = soup.select('a.screener-pages')
    if not tags:
        return 1
    else:
        return int(tags[-1].get_text())


def get_tickers(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    tickers = soup.select('body > tr > td > div#screener-content > table > tr > td > table > tr > td:nth-of-type(1) > span')
    for ticker in tickers:
        TICKERS.append(ticker.get_text().replace(u'\xa0', u''))
    return len(tickers)


def parse():
    html = get_page_html(URL)
    if html.status_code == 200:
        pages_count = get_paging_count(html)
        counter = 0
        for page in range(1, pages_count + 1):
            current_html = get_page_html(URL, params={'r': counter})
            counter += get_tickers(current_html) + 1
        print(TICKERS)
    else:
        print('Something goes wrong. Status code: ' + html.status_code)


def main():
    if get_commandline_args().cheap and get_commandline_args().expensive:
        print(f"{b_colors.FAIL}Warning: \nYou can\'t get cheap and expensive tickers both!{b_colors.ENDC}")
        # From POSIX standard - https://docs.python.org/2/library/os.html#process-management
        sys.exit(os.EX_SOFTWARE)
    elif get_commandline_args().cheap:
        global URL
        URL = CHEAP_URL
        parse()
    elif get_commandline_args().expensive:
        URL = EXPENSIVE_URL
        parse()
    elif get_commandline_args().link is not None:
        if validators.url(get_commandline_args().link) and validate_finviz_url(get_commandline_args().link):
            URL = get_commandline_args().link
            parse()
        else:
            print(
                f"{b_colors.FAIL}Warning: \nNot valid URL is set, please check this link and try again.{b_colors.ENDC}")
    else:
        print(f"{b_colors.FAIL}Warning: \nNo one params not be established, please check -h or --help {b_colors.ENDC}")
        # From POSIX standard - https://docs.python.org/2/library/os.html#process-management
        sys.exit(os.EX_SOFTWARE)


if __name__ == '__main__':
    # https://finviz.com/screener.ashx?v=111
    URL = ''
    CHEAP_URL = 'https://finviz.com/screener.ashx?v=411&f=geo_usa,ind_stocksonly,sh_avgvol_o300,sh_curvol_o300,sh_price_u10,ta_averagetruerange_o0.25'
    EXPENSIVE_URL = 'https://finviz.com/screener.ashx?v=411&f=geo_usa,ind_stocksonly,sh_avgvol_o300,sh_curvol_o300,sh_price_o10,ta_averagetruerange_o1'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Arch; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    TICKERS = []
    main()
