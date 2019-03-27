# python2 libraries (mechanize)
from bs4 import BeautifulSoup
import os
import matplotlib.pyplot as plt
from natsort import natsorted
import numpy as np
from glob import *

import time
import datetime
import pytz


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
    last_update_datetime = entries[-1].get_text()[-20:-1]
    entries = entries[2:-2]
    
    data = [] # (u'...' strings)
    for entry in entries: # rank, team name, number of tournaments, score
        rank = entry.find_all('td')[0].get_text()[:-1]
        team_name = entry.find_all('td')[2].get_text()
        n_tournaments = entry.find_all('td')[4].get_text()
        score = entry.find_all('td')[5].get_text()
        data.append([rank,team_name,n_tournaments,score])
    
    return data, last_update_datetime

def plot_team_progression(directory,team_name_list):
    ### rank/score of a team(s) over time
    # gather files list
    files_list = natsorted(glob(directory+'/ranking_????-??-??_??:??:??.html')) # natsort should give roughly the right order
    
    # prepare data structure
    rank = np.zeros((len(files_list),len(team_name_list)))
    score = np.zeros((len(files_list),len(team_name_list)))
    update_datetime = np.zeros((len(files_list),1))
    update_datetime = []
    
    # gather data
    for i,f in enumerate(files_list):
        data,update = process_html_tournament_table(f)
        update_datetime.append(update)
        for j,team_name in enumerate(team_name_list):
            for d in data:
                if d[1]==team_name:
                    rank[i,j] = d[0]
                    score[i,j] = d[3]
                    break
    
    # thin out data (according to updates)
    new = np.zeros(len(update_datetime),dtype=np.int)
    new[0] = 1
    for i in range(1,len(new)):
        if update_datetime[i] != update_datetime[i-1]:
            new[i] = 1
    
    rank = rank[new==1,:]
    score = score[new==1,:]
    #update_datetime = update_datetime[new==1] # not sure how to label the axis anyways
    
    # plot
    # implement color set,
    fig,(ax1,ax2) = plt.subplots(1,2,figsize=(9,4.5),tight_layout=True,dpi=100)
    ax1.set_xlabel('time')
    ax1.set_ylabel('rank')
    for j,team_name in enumerate(team_name_list):
        ax1.plot(range(len(rank[:,0])),rank[:,j],'-ko',label=team_name)
    ax1.legend(loc='best')
    
    ax2.set_xlabel('time')
    ax2.set_ylabel('score')
    for j,team_name in enumerate(team_name_list):
        ax2.plot(range(len(score[:,0])),score[:,j],'-ko',label=team_name)
    ax2.legend(loc='best')
    ax2.set_ylim((0,None))
    
    #plt.savefig(+'.png')
    plt.show()
    plt.close()
    
    
def plot_score_top_x(directory,x):
    ### score of the best x teams over time
    ### the best x teams changing over time. could do at start of data? or just list of team_names?
    # gather files list
    files_list = natsorted(glob(directory+'/ranking_????-??-??_??:??:??.html')) # natsort should give roughly the right order
    
    # prepare data structure
    score = np.zeros((len(files_list),x))
    update_datetime = np.zeros((len(files_list),1))
    update_datetime = []
    
    # gather data
    for i,f in enumerate(files_list):
        data,update = process_html_tournament_table(f)
        update_datetime.append(update)
        for j in range(x):
            score[i,j] = data[j][3]

    # thin out data (according to updates)
    
    
    # plot
    print(score)
    


plot_team_progression('/home/richard/Documents/jtr_ranking_scrape/ranking_scraper-raw_data/',['Rigor Mortis','Zonenkinder','Gossenhauer','TackleTiger'])   
#plot_score_top_x('/home/richard/Documents/jtr_ranking_scrape/ranking_scraper-raw_data/',8)



# rank / score of a team / the best x teams over time

# some form of statistic on score: average among top teams, threashold for topX positions, total (sum) score, ...?

# I sample way more often than the website gets updated -> thin out data before plotting by this frequency (and also date correctly!)
