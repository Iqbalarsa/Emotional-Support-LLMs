# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 18:01:20 2026

@author: Asus
"""
import requests
import pandas as pd
import time
subreddits_lang = ['espanol', 'Espana', 'mexico', 'Colombia', 'PERU', 'argentina', 'vzla', 'ecuador', 'guatemala', 'BOLIVIA']
subreddits_health = ['Anxiety', 'depression', 'bipolar', 'autism', 'schizofrenia','mentalhealth']

keyword_lang = ['depresión', 'ansiedad', 'bipolar', 'autismo', 'esquizofrenia', 'triste', 'salud mental', 'trauma']
keyword_health = ['depresión', 'ansiedad', 'español', 'bipolar', 'latino', 'autismo', 'esquizofrenia', 'triste', 'salud mental', 'trauma']
subreddit = subreddits_lang[0]
keyword = keyword_lang[0]

def get_reddit_data(subreddit,keyword):
    print(subreddit,keyword)
    url = f'https://www.reddit.com/r/{subreddit}/search.json?q={keyword}&restrict_sr=on'
    content = requests.get(url, headers = {'User-agent':'Student'}).json()
    posts = content['data']['children']
    
    rows = []
    for x in posts:
        rows.append([subreddit,keyword,x['data']['id'], x['data']['title'],x['data']['selftext']])

    return rows 

results = []
for sub in subreddits_lang:
    for key in keyword_lang:
        results = results + get_reddit_data(sub,key)
        time.sleep(8)

for sub in subreddits_health:
    for key in keyword_health:
        results = results + get_reddit_data(sub,key)
        time.sleep(8)

df = pd.DataFrame(columns=['subreddit', 'keyword', 'id', 'title', 'text'],data=results)
df.to_csv("all_subreddits.csv",encoding='utf-8-sig', index=False)
