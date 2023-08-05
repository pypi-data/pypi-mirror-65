from bs4 import BeautifulSoup
import requests
import re


def print_problems(all):
    for x in all:
        z = x.find_all_next('div', attrs={'class', 'panel historypanel'})[:3]
        for prob in z:
            links = prob.find_all('a')
            cpid = None
            id = None
            for e_ in links:
                e = e_['href']
                if e.startswith('index.php'):
                    g = re.match(r'.*cpid=(\d+).*', e)
                    cpid = g.group(1)
                if e.startswith('current'):
                    if e.endswith('html'):
                        g = re.match(r'.*sol_([^.]*)\.html', e)
                        id = g.group(1)
            print('%s;%d;%s;%s;%s;%s;%s' % (month, year, x.text, prob.find('b').text, cpid, id,
                                            ';'.join('http://usaco.org/' + x['href'] for x in links)))


for year in range(2011, 2015):
    for month in ['jan', 'feb', 'open', 'nov', 'dec']:
        link = 'http://usaco.org/index.php?page=%s%dproblems' % (month, year % 100)
        r = requests.get(link)
        parser = BeautifulSoup(r.text, 'html.parser')
        print_problems(parser.find_all('h2'))
for year in range(2014, 2021):
    for month in ['jan', 'feb', 'open', 'dec']:
        link = 'http://usaco.org/index.php?page=%s%dresults' % (month, year % 100)
        r = requests.get(link)
        parser = BeautifulSoup(r.text, 'html.parser')
        print_problems([x.parent for x in parser.select('h2 img')])

