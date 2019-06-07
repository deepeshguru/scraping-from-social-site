# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:24:53 2019

@author: Deepesh  Agrawal
"""

import time
import pandas as pd
from selenium import webdriver
import requests

post_want = 10

data_1 = {}
twitter_profille = ["http://twitter.com/BarackObama/", "http://twitter.com/justinbieber/"]
insta_profile = ["https://www.instagram.com/cristiano/", "https://www.instagram.com/arianagrande/"]

data_1["instagram"] = {}
data_1["twitter"] = {}

count = 1

for profile in insta_profile:
    driver = webdriver.Chrome(executable_path=r"C:\Users\tvs13\Downloads\chromedriver.exe")
    source = profile
    name = source.split("/")[-2]
    driver.get(source)
    
    driver.maximize_window()
    
    from bs4 import BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    li = soup.find_all("li", class_="Y8-fY ")
    no_of_posts = li[0].text
    no_of_followers = li[1].text
    no_of_following = li[2].text
    
    
    links = []
    
    post_row = soup.find_all("div", class_="Nnq7C weEfm")
    
    for posts in post_row:
        for post in posts:
            links.append("https://www.instagram.com/instagram" + post.find("a")['href'])
    
    SCROLL_PAUSE_TIME = 10
    
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while(1):    # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        post_row = soup.find_all("div", class_="Nnq7C weEfm")
    
        for posts in post_row:
            for post in posts:
                links.append("https://www.instagram.com/instagram" + post.find("a")['href'])
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if len(set(links))>=post_want:
            break
        if new_height == last_height:
            break
        last_height = new_height    
        
    driver.quit()    
    link = []
    for i in range(1, len(links)+1):
        if links[i-1] not in links[i:]:
            link.append(links[i-1])
    
    
    
    content = []
        
    for i in link[:min(post_want, len(link))]:
        driver = webdriver.Chrome(executable_path=r"C:\Users\tvs13\Downloads\chromedriver.exe")
        temp = []
        driver.get(i)
        time.sleep(5)
        html = driver.page_source
        
        soup = BeautifulSoup(html, 'lxml')
        
        
        try:
            post_views = soup.find("span", class_="vcOH2").text
            post_likes = ""
        except:
            post_likes = soup.find("div", class_="Nm9Fw").text
            post_views = ""
        try:
            div = soup.find("div", "C4VMK")
            span = div.find_all("span")
            post_text = span[1].text
        except:
            try: 
                post_text = span[0].text
            except:
                post_text = ""
        src = soup.find("div", class_="_5wCQW")
        try:
            video = src.find("video")['src']
        except:
            video = ""
        try:
            image = src.find("img")['src']
        except:
            try:
                image = soup.find("img", class_="FFVAD")['srcset'].split()[0]
            except:
                image = ""
        
        driver.quit()
        content.append([post_text, post_views, post_likes, image, video])
    
    
    data_1["instagram"]["Profile " + str(count)] = {"Name": name, "Total posts": no_of_posts, 
                                                  "followers": no_of_followers,
                                                  "following": no_of_following}
    
    data_1["instagram"]["Profile " + str(count)]['post_infos'] = {}
    
    for i in range(post_want):
        data_1["instagram"]["Profile " + str(count)]['post_infos'][str(i+1)] = {"post caption": content[i][0], 
                                                                              "like on post": content[i][2],
                                                                              "views on post": content[i][1], 
                                                                              "image link": content[i][3], 
                                                                              "video link": content[i][4]}
    count = count + 1
        

count = 1


for profile in twitter_profille:
    source = profile
    data = []
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
        
    
    data_1["twitter"]["Profile " + str(count)] = {"Name": name,
                                                "Total tweets": tweets, 
                                                "Following": following, 
                                                "Followers": followers, 
                                                "Likes": likes}
    
    data_1["twitter"]["Profile " + str(count)]["post infos"]={}
    
    for i in range(min(len(df), post_want)):
        data_1["twitter"]["Profile " + str(count)]["post infos"][str(i+1)] = {"post": df.iloc[i, 0], 
                                                                            "Reply": df.iloc[i, 1],
                                                                            "Retweet": df.iloc[i, 2], 
                                                                            "Like": df.iloc[i, 3]}
    driver.quit()


import json

with open('insta_twitter.json', 'w') as fp:
    json.dump(data_1, fp)


with open('D:\Machine Learning\scraping\data.json', 'rb') as f:
    r = requests.post('http://127.0.0.1:5000/post', files={'upload': f})













