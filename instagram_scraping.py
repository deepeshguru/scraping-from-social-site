# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:30:27 2019

@author: Deepesh  Agrawal
"""

import time
from selenium import webdriver
driver = webdriver.Chrome(executable_path=r"C:\Users\tvs13\Downloads\chromedriver.exe")

post_want = 50

source = "https://www.instagram.com/instagram/"
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
    div = driver.find_element_by_class_name("C4VMK")
    html = driver.page_source
    
    soup = BeautifulSoup(html, 'lxml')
    
    div = soup.find("div", "C4VMK")
    span = div.find_all("span")
    try:
        post_views = soup.find("span", class_="vcOH2").text
        post_likes = ""
    except:
        post_likes = soup.find("div", class_="Nm9Fw").text
        post_views = ""
    try:
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


data = {"Name": name, "Total posts": no_of_posts, "followers": no_of_followers,
        "following": no_of_following}

data['post_infos'] = {}

for i in range(post_want):
    data['post_infos'][str(i+1)] = {"post caption": content[i][0], "like on post": content[i][2],
        "views on post": content[i][1], "image link": content[i][3], "video link": content[i][4]}


import json

with open('data.json', 'w') as fp:
    json.dump(data, fp)
















