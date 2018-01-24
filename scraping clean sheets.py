# program to scrape clean sheet odds and store them in an excel file

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

def to_float(a):
    if a == 'evens':
        a = 2.0
    else:
        a = a.split('/')
        a = (float(a[0]) / float(a[1])) + 1
    return a


my_url = 'http://www.paddypower.com/football/football-matches/premier-league?ev_oc_grp_ids=9551'


def get_html(url):
    Client = urlopen(url)
    page_html = Client.read()
    Client.close()
    page_soup = soup(page_html, 'html.parser')
    return page_soup


def team_odds_dict():
    team_abbv = {'West Ham ': 'WHU', 'Tottenham ': 'TOT', 'Burnley ': 'BRN', 'Huddersfield ': 'HUD', 'Everton ': 'EVE', 'Bournemouth ': 'BOU', 'Man City ': 'MCI',
                 'Crystal Palace ': 'CRY', 'Southampton ': 'SOU', 'Man Utd ': 'MUN', 'Stoke ': 'STK', 'Chelsea ': 'CHE', 'Swansea ': 'SWA', 'Watford ': 'WAT',
                 'Leicester ': 'LEI', 'Liverpool ': 'LIV', 'Brighton ': 'BHA', 'Newcastle ': 'NEW', 'Arsenal ': 'ARS', 'West Brom ': 'WBA'}

    team_dict = {}
    soup = get_html(my_url)
    for i in team_abbv.keys():
        team = soup.find(text=i)
        odds = to_float(team.parent.parent.find('span', {'class': 'odds-value'}).text)
        team = team_abbv[team]
        team_dict[team] = odds
    return team_dict


print(team_odds_dict())
