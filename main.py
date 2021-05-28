import urllib.request
import csv
from bs4 import BeautifulSoup
from Extractor import extracter, find_all
from tqdm import tqdm

start = urllib.request.urlopen("https://www.baseball-reference.com/leagues/MLB/2021-schedule.shtml")
soup = BeautifulSoup(start.read().decode(), 'lxml')
rows = soup.find_all('p', class_='game')
games = []
header = ['away_AB', 'away_R', 'away_H', 'away_RBI', 'away_BB', 'away_SO', 'away_PA', 'away_BA', 'away_OBP', 'away_SLG'
    , 'away_OPS', 'away_p_H', 'away_p_R', 'away_p_ER', 'away_pBB', 'away_p_SO', 'away_p_ERA', 'home_AB', 'home_R',
          'home_H',
          'home_RBI', 'home_BB', 'home_SO', 'home_PA', 'home_BA', 'home_OBP', 'home_SLG', 'home_OPS', 'home_p_H',
          'home_p_R',
          'home_p_ER', 'home_pBB', 'home_p_SO', 'home_p_ERA', 'home_win']
req1 = ['AB', 'R', 'H', 'RBI', 'BB', 'SO', 'PA', 'batting_avg', 'onbase_perc', 'slugging_perc', 'onbase_plus_slugging']
req2 = ['H', 'R', 'ER', 'BB', 'SO', 'earned_run_avg']
entry = [header]

count = 0
for row in rows:
    if row.find_all('a')[-1].text == "Boxscore":
        games.append(row)
nos = int(input(f'How many games({len(games)}) to get(from top)? : '))
for game in tqdm(games[:nos]):
    count += 1
    gamelink = 'https://www.baseball-reference.com' + game.find_all('a')[-1]['href']
    # gamedata = urllib.request.urlopen('https://www.baseball-reference.com/boxes/ANA/ANA202104010.shtml')
    gamedata = urllib.request.urlopen(gamelink)
    soup2 = BeautifulSoup(gamedata.read().decode(), 'lxml')
    raw = str(soup2)

    awayitems = []
    homeitems = []
    for i in req1:
        awayitems.append(extracter(i, 0, raw))
        homeitems.append(extracter(i, 1, raw))
    awayitems_p = []
    homeitems_p = []
    for i in req2:
        awayitems_p.append(extracter(i, 2, raw))
        homeitems_p.append(extracter(i, 3, raw))

    # find who won
    h = list(find_all(raw, 'itemprop="performer"'))
    awayscore = int(raw[h[0]:h[0]+750][raw[h[0]:h[0]+750].find('class="score">')+14:raw[h[0]:h[0]+750].find('class="score">')+15])
    homescore = int(raw[h[1]:h[1]+750][raw[h[1]:h[1]+750].find('class="score">')+14:raw[h[1]:h[1]+750].find('class="score">')+15])

    result = [True if (homescore>awayscore) else False]
    data = awayitems + awayitems_p + homeitems + homeitems_p + result
    entry.append(data)
with open("gamedata.csv", "w") as fp:
    wr = csv.writer(fp, lineterminator='\n')
    wr.writerows(entry)
