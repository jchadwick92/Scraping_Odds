from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import re


def get_html(url):
    Client = urlopen(url)
    page_html = Client.read()
    Client.close()
    page_soup = soup(page_html, 'html.parser')
    return page_soup


def clean_sheet_odds():
    team_abbv = {'West Ham': 'WHU', 'Tottenham': 'TOT', 'Burnley': 'BRN', 'Huddersfield': 'HUD', 'Everton': 'EVE', 'Bournemouth': 'BOU', 'Man City': 'MCI',
                   'Crystal Palace': 'CRY', 'Southampton': 'SOU', 'Man Utd': 'MUN', 'Stoke': 'STK', 'Chelsea': 'CHE', 'Swansea': 'SWA', 'Watford': 'WAT',
                   'Leicester': 'LEI', 'Liverpool': 'LIV', 'Brighton': 'BHA', 'Newcastle': 'NEW', 'Arsenal': 'ARS', 'West Brom': 'WBA'}
    team_dict = {}
    soup = get_html('http://sports.williamhill.com/bet/en-gb/betting/g/158525/To+Keep+a+Clean+Sheet.html')
    matches = soup.find_all('div', {'class':'marketHolderExpanded'})

    for match in matches[:10]:
        teams = match.find_all('div', {'id': re.compile('^ip_oc_desc_')})
        odds = match.find_all('div', {'class': 'eventprice'})

        team_dict[team_abbv[teams[0].text.strip()]] = to_float(odds[0].text.strip())
        team_dict[team_abbv[teams[1].text.strip()]] = to_float(odds[1].text.strip())

    return team_dict


def to_float(a):
    if a == 'evens':
        a = 2.0
    elif a == 'EVS':
        a = 2.0
    else:
        a = a.split('/')
        a = (float(a[0]) / float(a[1]))
    return a


print(clean_sheet_odds())
