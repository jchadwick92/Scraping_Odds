from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd

def get_html(url):
    Client = urlopen(url)
    page_html = Client.read()
    Client.close()
    page_soup = soup(page_html, 'html.parser')
    return page_soup


def match_odds():
    team_abbv = {'West Ham': 'WHU', 'Tottenham': 'TOT', 'Burnley': 'BRN', 'Huddersfield': 'HUD', 'Everton': 'EVE', 'Bournemouth': 'BOU', 'Man City': 'MCI',
                 'Crystal Palace': 'CRY', 'Southampton': 'SOU', 'Man Utd': 'MUN', 'Stoke': 'STK', 'Chelsea': 'CHE', 'Swansea': 'SWA', 'Watford': 'WAT',
                 'Leicester': 'LEI', 'Liverpool': 'LIV', 'Brighton': 'BHA', 'Newcastle': 'NEW', 'Arsenal': 'ARS', 'West Brom': 'WBA'}
    team_dict = {}
    soup = get_html('https://www.oddschecker.com/football/english/premier-league')
    matches = soup.find_all('tr', {'class': 'match-on'})

    for match in matches[:10]:
        teams = match.find_all('span', {'class': 'fixtures-bet-name'})
        odds = match.find_all('span', {'class': 'odds'})

        team_dict[team_abbv[teams[0].text.strip()]] = to_float(odds[0].text.strip('( ) '))
        team_dict[team_abbv[teams[2].text.strip()]] = to_float(odds[2].text.strip('( ) '))

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


print(match_odds())
