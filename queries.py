# python2 libraries (mechanize)
import os
import numpy as np

import time
import datetime
import pytz

import webbrowser
import mechanize


def process_html_tournament_table(filename):
    # ranking table:
        #<td>1.</td> # rank
        #<td style="text-align: center;"><img src="icons/arrow-same.png" alt="" /></td> # change indicator
        #<td><a href="list.team.info.php?id=3" title="Rigor Mortis">Rigor Mortis</a></td> # team name
        #<td><img src="flags/deutschland.gif" alt="Deutschland" title="Deutschland" /> Berlin</td> # country, city
        #<td>83</td> # number of tournaments
        #<td>15.77</td> # score
    # last updated datetime:
        #<td colspan="6">Letzte Aktualisierung: 2019-03-17 01:17:16</td>
    with open(filename) as fp:
        soup = BeautifulSoup(fp,'html.parser')
    
    
    entries = soup.find_all('tr')
    last_update_datetime = entries[-1].get_text()[-20:]
    entries = entries[2:-2]
    
    data = [] # (u'...' strings)
    for entry in entries: # rank, team name, number of tournaments, score
        rank = entry.find_all('td')[0].get_text()[:-1]
        team_name = entry.find_all('td')[2].get_text()
        n_tournaments = entry.find_all('td')[4].get_text()
        score = entry.find_all('td')[5].get_text()
        data.append([rank,team_name,n_tournaments,score])
    
    return data, last_update_datetime
