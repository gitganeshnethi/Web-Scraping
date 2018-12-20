# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:08:22 2018

@author: Ganesh NP
"""
#installing selenium package
!pip install selenium
import os
import pandas as pd
import time
import datetime
import seaborn
import matplotlib.pyplot as plt 


os.getcwd()  
#driver exe should be copied to current dir
os.chdir('C:\\Users\\Administrator\\Scraping'

from selenium import webdriver     
browser = webdriver.Chrome('chromedriver.exe')   
url = 'https://www.cricbuzz.com/live-cricket-scores/20302/aus-vs-ind-2nd-test-india-tour-of-australia-2018-19'
browser.get(url)
parents  = browser.find_elements_by_css_selector('div.cb-col.cb-col-100.ng-scope')
#print(parents)
#len(parents)

data_commentary = pd.DataFrame()

for parent in parents:
    try:
        ball_number = parent.find_element_by_css_selector('div.cb-ovr-num')
        date_time = ball_number.get_attribute('title')
        ball_number = ball_number.get_attribute('innerHTML')
        
        
        comment = parent.find_element_by_css_selector('p.cb-com-ln')
        comment = comment.get_attribute('innerHTML')
                
        #print(ball_number,' | ',date_time)
        #print(comment)
        data_commentary = data_commentary.append({
                'Ball-Number':ball_number,
                'Date and Time':date_time,
                'Commentary':comment},ignore_index=True)

    except:
        pass 
    
    #print('-----------------------------')
 
data_commentary

#-----------------------------------------------------------------
#trying scraping for more pages at at time with click more button
#-----------------------------------------------------------------
url = 'https://www.cricbuzz.com/live-cricket-scores/20302/aus-vs-ind-2nd-test-india-tour-of-australia-2018-19'
browser.get(url)
time.sleep(5)
for i in range(50):
    browser.find_element_by_css_selector('a.cb-com-lod-mr').click()
    time.sleep(5)

parents  = browser.find_elements_by_css_selector('div.cb-col.cb-col-100.ng-scope')
#print(parents)
#len(parents)

data_commentary = pd.DataFrame()

for parent in parents:
    try:
        ball_number = parent.find_element_by_css_selector('div.cb-ovr-num')
        date_time = ball_number.get_attribute('title')
        ball_number = ball_number.get_attribute('innerHTML')
        
        
        comment = parent.find_element_by_css_selector('p.cb-com-ln')
        comment = comment.get_attribute('innerHTML')
                
        #print(ball_number,' | ',date_time)
        #print(comment)
        data_commentary = data_commentary.append({
                'Ball-Number':ball_number,
                'Date and Time':date_time,
                'Commentary':comment},ignore_index=True)

    except:
        pass 
    
    #print('-----------------------------')
 
data_commentary
data_commentary.shape

#1. Separate over and ball number in to two columns
#2. Identify ballwise runs
#3. Identify type of extras
#4. Create a new column called extra. Value will be 1 if it is extra else 0

 #1. Separate over and ball number in to two columns
data_commentary['over'] = data_commentary['Ball-Number'].str.split('.').apply(lambda x:x[0]).astype(int)
data_commentary['ball'] = data_commentary['Ball-Number'].str.split('.').apply(lambda x:x[1]).astype(int)
data_commentary[['Ball-Number','over','ball','Commentary']]


#2. Identify ballwise runs
def extract_run(Commentary):
    if '1 run' in Commentary:
        return 1
    elif '2 runs' in Commentary:
        return 2
    elif '3 runs' in Commentary:
        return 3
    elif '<b>FOUR</b>' in Commentary:
        return 4
    elif '<b>SIX</b>' in Commentary:
        return 6
    elif '5 runs' in Commentary:
        return 5
    elif 'no run' in Commentary:
        return 0
    else:
        return float('nan')
data_commentary['runs'] = data_commentary['Commentary'].apply(extract_run)
data_commentary

#3. Identify type of extras
def abc(Commentary):
    if '<b>out</b>' in Commentary:
        return 'W'
    elif '<b>wide</b>' in Commentary:
        return 'WD'
    elif 'byes, 1 run' in Commentary:
        return '1B'
    elif 'byes, <b>FOUR</b>' in Commentary:
        return '4B'
    elif 'byes, 2 runs' in Commentary:
        return '2B'
    elif 'byes, 3 runs' in Commentary:
        return '3B'
    #elif 'leg byes <b>FOUR</b>' in Commentary:
        #return '4L'
    #elif ',leg byes, 1 run' in Commentary:
        #return '1L'
    #elif 'leg byes, 2 runs' in Commentary:
        #return '2L'
    #elif 'leg byes, 3 runs' in Commentary:
        #return '3L'
    elif '<b>no ball</b>' in Commentary:
        return 'NB'
    else:
        return float('nan')
data_commentary['happend_on_ball'] = data_commentary['Commentary'].apply(abc)
data_commentary.to_csv('cricbuz1.csv',index=False)

data_commentary['runs'].value_counts()

#4. Create a new column called extra. Value will be 1 if it is extra else 0
def extra(happend_on_ball):
    if happend_on_ball=='WD' or happend_on_ball=='1B' or happend_on_ball=='2B' or happend_on_ball=='NB' or happend_on_ball=='3B' or happend_on_ball=='4B':
        return 1
    else:
        return 0
data_commentary['extra'] = data_commentary['happend_on_ball'].apply(extra)
data_commentary



#-----------------------------------
#converting scraped date and time to date and time pandas format
data_commentary['Date and Time'] = pd.to_datetime(data_commentary['Date and Time'])

#MIN AND MAX OF DATE
data_commentary['Date and Time'].min(), data_commentary['Date and Time'].max()   
  
#Creating new column called day after extracting day from date and time column
data_commentary['day'] = data_commentary['Date and Time'].dt.day

#storing data with respect to play happend on each day
day1 = data_commentary[data_commentary['day']==14]
day2 = data_commentary[data_commentary['day']==15]
day3 = data_commentary[data_commentary['day']==16]
day4 = data_commentary[data_commentary['day']==17]
day5 = data_commentary[data_commentary['day']==18]

day4.shape
day4.columns
#we create pivot table for day4 data
day4_pivot = day4.pivot_table(index='ball',
                              columns='over',
                              values='runs')


#plotting for pivot table
plt.figure(figsize=(20,7))
seaborn.heatmap(day4_pivot,cmap='Oranges')
