# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 15:19:21 2019

@author: Deepesh Agrawal
"""

import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import datetime
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from dateutil.parser import parse
import pandas as pd
import requests
import getpass



def ip():
    Source = requests.get('https://free-proxy-list.net/').text

    soup = BeautifulSoup(Source, 'html5lib')

    tables = soup.find_all("table")

    tbody = tables[0].find("tbody")
    thead = tables[0].find("thead")

    colums = thead.find_all("th")

    cols = []

    for i in colums:
        cols.append(i.text)
        
    data = []
    for tr in tbody.find_all("tr"):
        row = []
        for td in tr.find_all("td"):
            row.append(td.text)
        data.append(row)


    df = pd.DataFrame(data, columns=cols)

    df = df[df["Https"]=="yes"]
    return df

df = ip()

def more_ip():
    Source = requests.get('https://www.proxynova.com/proxy-server-list/country-in/').text
    
    soup = BeautifulSoup(Source, 'lxml')
    
    tbody = soup.find("tbody")
    
    trs = tbody.find_all("tr")
    
    address = []
    ports = []
    for tr in trs:
        tds = tr.find_all("td")
        if len(tds)>1:
            ports.append(str(int(tds[1].text)))
            anom = tds[6].text
        td1 = str(tds[0])
        i = td1.find("title=")
        td1 = td1[i+7:].replace("-", ' ')
        td1 = td1.replace('"', ' ')
        td1 = td1.split()
        td1 = td1[0]
        x = list(range(9))
        #print(tds[1].text)
        try :
            if int(td1[0]) in x and anom.replace('\n','') != 'Transparent':
                td1 = td1.split('.')
                td1 = '.'.join(td1[:4])
                address.append(td1+':'+str(int(tds[1].text)))
                print(anom)
        except:
            pass
        return df


def good_proxy(dff, source):
    for i in range(len(dff)):
        try:
            proxies = {
                'http': dff.iloc[i, 0]+":"+dff.iloc[i+1, 1],
                'https': dff.iloc[i, 0]+":"+dff.iloc[i+1, 1],
            }
            
            # Create the session and set the proxies.
            s = requests.Session()
            s.proxies = proxies
            #Source = requests.get('https://free-proxy-list.net/')
            # Make the HTTP request through the session.
            r = s.get('https://www.facebook.com/')
            
            # Check if the proxy was indeed used (the text should contain the proxy IP).
            print(r.text)
            print(r.status_code)
            print(proxies)
            PROXY = proxies['https']
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % PROXY)
            chrome_options.add_argument("--disable-notifications")
            
            driver = webdriver.Chrome(executable_path=r"C:\Users\Raushan\Downloads\chromedriver_win32\chromedriver.exe", options=chrome_options)
            driver.delete_all_cookies()
            driver.get(source)
            html = driver.page_source
            
            if "No internet" in html:
                continue
            
            return proxies['https']
            '''if h1 != 'No internet':
                driver.quit()
                return proxies['http']
            else:
                print('trying')
                driver.quit()
                good_proxy(dff, source)'''
        except Exception as e:
                print(e)
        return proxies['https']
    
    




post_want = 5

source_links = pd.read_excel(r"E:\python_codes\links_insta_twitter.xlsx")
data_1 = {}
twitter_profille = []
insta_profile = []
facebook_profile = []


for i in range(len(source_links)):
    x = source_links.iloc[i, 0].split("/")[2]
    if 'twitter.com' == x:
        twitter_profille.append(source_links.iloc[i, 0])
    elif 'www.instagram.com' == x:
        insta_profile.append(source_links.iloc[i, 0])
    elif 'www.facebook.com' == x:
        facebook_profile.append(source_links.iloc[i, 0])

while(1):
    x = str(datetime.datetime.now().time()).split(":")
    x[2] = int(float(x[2]))
    y = str(datetime.time(17, 42, 0, 0)).split(":")
    y[2] = int(y[2])
    if x == y:
        print("True")
        data_1 = {}
        
        data_1["facebook"] = {}
        data_1["instagram"] = {}
        data_1["twitter"] = {}
        
        count = 1
        for profile in facebook_profile:
            source = profile
            #usr=input('Enter Email Id:') 
            #pwd=getpass.getpass('Enter Password:') 
            PROXY = good_proxy(more_ip(), source)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server=%s' % PROXY)
            chrome_options.add_argument("--disable-notifications")
            
            driver = webdriver.Chrome(executable_path=r"C:\Users\Raushan\Downloads\chromedriver_win32\chromedriver.exe", options=chrome_options)
            driver.delete_all_cookies()
            driver.get(source) 
            name = source.split('/')[-2]
            print ("Opened facebook") 
            sleep(1) 
            
            
            html = driver.page_source
            
            soup = BeautifulSoup(html, 'html5lib')
            lnf = soup.find_all("div", class_="_4bl9")
            for i in lnf:
                print(i.text)
            
            likes_on_page = lnf[2].text
            follows_on_page = lnf[3].text
            
            
            
            
            
            print("Going to post page")
            driver.get(source + 'posts/') 
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            driver.find_element_by_class_name("_3j0u").click()
            
            SCROLL_PAUSE_TIME = 0.5
            
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            for i in range(2):
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
                # Wait to load page
                time.sleep(10)
            
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                html = driver.page_source
                
                soup = BeautifulSoup(html, 'html5lib')
                posts = soup.find_all("div", class_="_4-u2 _4-u8")
                if len(posts) >= post_want:
                    break
                if new_height == last_height:
                    break
                last_height = new_height
                
                
                
            
            html = driver.page_source
            
            soup = BeautifulSoup(html, 'html5lib')
            posts = soup.find_all("div", class_="_4-u2 _4-u8")
            
            post_content = []
            likes = []
            links = []
            comment_share_view = []
            
            
            
            
            for post in posts:
                try:
                    content = post.find("div", class_="_5pbx userContent _3576")
                    post_content.append(content.text)
                    try:
                        like = post.find("div", class_="_66lg")
                        likes.append(like.text[:int(len(like.text)/2)])
                    except:
                        try:
                            like = post.find("div", class_="UFILikeSentenceText")
                            likes.append(like.text)
                        except:
                            pass
                    try:
                        share = post.find("div", class_="UFIRow UFIShareRow")
                        view = post.find("div", class_="_1t6k")
                        comment_share_view.append([share.text, view.text])
                    except:
                        try:
                            cnsnv = post.find("div", class_="_4vn1")
                            comment_share_view.append(cnsnv.text)
                        except:
                            pass
                    try:
                        image_div = post.find("div", class_="_3x-2")
                        image = image_div.find_all("a", href=True)
                    
                        try:
                            if image[0]['href'][:4] != 'http':
                                links.append('https://www.facebook.com' + image[0]['href'])
                            else:
                                links.append(image[0]['href'])
                        except:
                            links.append(None)
                    except:
                        pass
                except:
                    try:
                        content = post.find("div", class_="_5pbx userContent _3ds9 _3576")
                        post_content.append(content.text)
                        try:
                            like = post.find("div", class_="_66lg")
                            likes.append(like.text[:int(len(like.text)/2)])
                        except:
                            try:
                                like = post.find("div", class_="UFILikeSentenceText")
                                likes.append(like.text)
                            except:
                                pass
                        try:
                            share = post.find("div", class_="UFIRow UFIShareRow")
                            view = post.find("div", class_="_1t6k")
                            comment_share_view.append([share.text, view.text])
                        except:
                            try:
                                cnsnv = post.find("div", class_="_4vn1")
                                comment_share_view.append(cnsnv.text)
                            except:
                                pass
                        try:
                            image_div = post.find("div", class_="_3x-2")
                            image = image_div.find_all("a", href=True)
                        
                            try:
                                if image[0]['href'][:4] != 'http':
                                    links.append('https://www.facebook.com' + image[0]['href'])
                                else:
                                    links.append(image[0]['href'])
                            except:
                                links.append(None)
                        except:
                            pass
                    except:
                        pass
            
            
            for i in range(len(likes)):
                if likes[i][-1] == "K":
                    likes[i] = float(likes[i][:-1]) * 1000
                elif likes[i][-1] == "M":
                    likes[i] = float(likes[i][:-1]) * 1000000
                elif likes[i].split()[-1] == "this.":
                    x = likes[i].split()
                    likes[i] = x[-4].replace(',', '')
            
            
            
            for i in range(len(comment_share_view)):
                if type(comment_share_view[i]) == str:
                    comment_share_view[i] = comment_share_view[i].replace('s','s ')
                elif type(comment_share_view[i]) == list:
                    comment_share_view[i] = ' '.join(comment_share_view[i])
            
            
            
            
            
            
            
            data_1["facebook"]["Profile " + str(count)] = {"Name": name,
                                                           "Likes on page": likes_on_page, 
                                                           "follows on page": follows_on_page}
            
            
            data_1["facebook"]["Profile " + str(count)]["post infos"]={}
            
            
            for i in range(min(len(likes), post_want)):
                
                data_1["facebook"]["Profile " + str(count)]["post infos"][i+1] = {"post": post_content[i], 
                               "Likes on post": likes[i],
                               "Platform": "Facebook",
                               "comments, shares and views on post": comment_share_view[i],
                               "links of image and video":links[i]}
            
            
            driver.delete_all_cookies()
            
            driver.quit()
            
            
            count = 1
            for profile in insta_profile:
                PROXY = good_proxy(more_ip(), source)
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--proxy-server=%s' % PROXY)
    
                driver = webdriver.Chrome(executable_path=r"C:\Users\Raushan\Downloads\chromedriver_win32\chromedriver.exe", 
                                          options=chrome_options)
                
                source = profile
                name = source.split("/")[-2]
                driver.get(source)
                
                driver.maximize_window()
                
                
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                li = soup.find_all("li", class_="Y8-fY")
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
                    
                    driver = webdriver.Chrome(executable_path=r"C:\Users\Raushan\Downloads\chromedriver_win32\chromedriver.exe")
                    
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
                
                PROXY = good_proxy(more_ip(), source)
                
                chrome_options = webdriver.ChromeOptions()
                
                chrome_options.add_argument('--proxy-server=%s' % PROXY)
    
                driver = webdriver.Chrome(executable_path=r"C:\Users\Raushan\Downloads\chromedriver_win32\chromedriver.exe", 
                                          options=chrome_options)
                source = profile
                data = []
                
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
            x = str(datetime.datetime.now()).split('.')[0].replace(':', '')
            with open('insta_twitter ' + x + '.json', 'w') as fp:
                json.dump(data_1, fp)
            try:
                with open(r'D:\Machine Learning\scraping\insta_twitter ' + x + '.json', 'rb') as f:
                    r = requests.post('http://127.0.0.1:5000/post', files={'upload': f})
                
                file = open("log.txt", "a+")
                file.write('insta_twitter ' + x + '.json' + '\t' + str(datetime.datetime.now()) + '\t' + str(r.status_code) + '\n')
                file.close()
                print('done')
            except:
                pass
    










