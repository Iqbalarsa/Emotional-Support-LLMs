# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:42:10 2026

@author: Asus
"""
import pandas as pd
import langdetect  

posts = pd.read_csv("all_subreddits.csv")
posts = posts.drop_duplicates(subset='id')
posts = posts.dropna()
first_person_pronuns = ['yo','mi','mí','conmigo','nosotros','nosotras','nos','mío','mía', 'me']

pattern = r'\b(' + '|'.join(first_person_pronuns) + r')\b'
posts = posts[posts.text.str.contains(pattern, case=False)]

def is_spanish(x):
    try:
        return langdetect.detect(x) == 'es'
    except Exception:        
        return False

posts = posts[posts.text.apply(is_spanish)]
email_regex_pattern = r'(?:[a-z0-9!#$%&''*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&''*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
phone_number_regex_pattern = r'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
posts = posts[posts.text.str.contains(email_regex_pattern,regex=True) == False]
posts = posts[posts.text.str.contains(phone_number_regex_pattern,regex=True) == False]
print(posts)
posts.to_csv("rule_based_filters.csv",encoding='utf-8-sig', index=False)