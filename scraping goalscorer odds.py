from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import sqlite3
import pandas as pd

conn = sqlite3.connect('football_stats.db')
c = conn.cursor()

def get_html(url):
    Client = urlopen(url)
    page_html = Client.read()
    Client.close()
    page_soup = soup(page_html, 'html.parser')
    return(page_soup)

def goalscorer_odds():
    Id_odds = {}
    soup = get_html('http://sports.williamhill.com/bet/en-gb/betting/g/348/Anytime+Goalscore')
    matches = soup.find_all('div', {'class':'marketHolderExpanded'})
    for match in matches:
        rows = match.find_all('tr', {'class': 'rowOdd'})
        for row in rows[1:]:
            name = row.find('td', {'class': 'leftPad'}).text.strip()
            odds = to_float(row.find('div', {'class': 'eventprice'}).text.strip())
            try:
                Id = find_player_id(name)
                Id_odds[Id] = odds
            except TypeError:
                pass     
    return(Id_odds)

def to_float(a):
    if a == 'evens':
        a = 2.0
    elif a == 'EVS':
        a = 2.0
    else:
        a = a.split('/')
        a = (float(a[0]) / float(a[1]))
    return(a)

def find_player_id(player):
    c.execute('SELECT id FROM idSkySportsName WHERE name=?', (player, ))
    return(c.fetchone()[0])



print(goalscorer_odds())

