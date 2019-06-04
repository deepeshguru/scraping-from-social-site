# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 15:01:12 2019

@author: tvs13
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd




post_want = 50

source = 'https://twitter.com/katyperry'

driver = webdriver.Chrome(executable_path=r"C:\Users\tvs13\Downloads\chromedriver.exe")

driver.get(source)
driver.maximize_window()

html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

ul = soup.find("ul", class_="ProfileNav-list")

lis = ul.find_all("li")

tweets = lis[0].text.split()[-1]

following = lis[1].text.split()[-1]


followers = lis[2].text.split()[-1]

likes = lis[3].text.split()[-1]

name = soup.find("a", class_="ProfileHeaderCard-nameLink u-textInheritColor js-nav").text

ol = soup.find("ol", class_="stream-items js-navigable-stream")

data = []

try:
    pinned = ol.find("li", class_="js-stream-item stream-item stream-item js-pinned ")
    
    pinned_tweet = list(set(ol.find("li", class_="js-stream-item stream-item stream-item js-pinned ").text.split('\n')))
    
    temp = [0] * 4
    
    temp = [0] * 4
    temp[0] = pinned.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    
    for j in pinned_tweet:
        if 'likes' in j:
            temp[3] = j
        elif 'retweets' in j:
            temp[2] = j
        elif 'replies' in j:
            temp[1] = j
    data.append(temp)
    
except:
    pass


lis = soup.find_all("li", class_="js-stream-item stream-item stream-item ")


for k in lis:
    temp = [0] * 4
    temp[0] = k.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    i = k.text
    i = i.split("\n")
    i = list(set(i))
    for j in i:
        if 'likes' in j:
            temp[3] = j
        elif 'retweets' in j:
            temp[2] = j
        elif 'replies' in j:
            temp[1] = j
    data.append(temp)



SCROLL_PAUSE_TIME = 10

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

new_data = []

while(1):    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find_all("li", class_="js-stream-item stream-item stream-item ")
    
    
    for k in lis:
        temp = [0] * 4
        temp[0] = k.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        i = k.text
        i = i.split("\n")
        i = list(set(i))
        for j in i:
            if 'likes' in j:
                temp[3] = j
            elif 'retweets' in j:
                temp[2] = j
            elif 'replies' in j:
                temp[1] = j
        data.append(temp)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    if len(df) >= post_want:
        break
    if new_height == last_height:
        break
    last_height = new_height    
    

data = {"Name": name, "Total tweets": tweets, "Following": following, "Followers": followers, "Likes": likes}

data["post infos"]={}

for i in range(min(len(df), post_want)):
    data["post infos"][str(i+1)] = {"post": df.iloc[i, 0], "Reply": df.iloc[i, 1],
                                    "Retweet": df.iloc[i, 2], "Like": df.iloc[i, 3]}


import json

with open(name+ '_' + 'twitter.json', 'w') as fp:
    json.dump(data, fp)



