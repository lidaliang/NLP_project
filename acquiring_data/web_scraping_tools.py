#We build tools to scrape a page of the cloudynights forum
#The input is a thread like 
#https://www.cloudynights.com/forum/67-refractors/?prune_day=100&sort_by=Z-A&sort_key=posts&topicfilter=all
#The output is a list of urls

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from datetime import datetime, timedelta
import os
import scipy
import re
import bs4
from bs4 import BeautifulSoup
import requests
import nltk
import pickle

def soup_a_forum(url,n_pages = 4):
    #n_pages needs to be smaller than the total number of pages in this forum
    soups = []
    page = 1
    title = ""
    while page <= n_pages:
        time.sleep(2)
        if page==1: page_url = url
        else: page_url = insert_mystr_before_astr(orgstr=url,mystr="page-"+str(page),astr="?prune_day")
        fpage1 = requests.get(page_url)
        soup1 = BeautifulSoup(fpage1.content, 'html.parser')
        
        #new_title = soup1.find_all('title')[0].get_text()
        #if title == new_title: break
        #else: title = new_title
        
        soups.append(soup1)
        page += 1
    return soups
    

def from_a_soup_to_url(soup):
    element_list = soup.find_all(id=re.compile("tid-link-......"))
    return [element["href"] for element in element_list] 

def remove_from_list_if_contains_substring(orglist,substring):
    return [ele for ele in orglist if not substring in ele] 

def remove_from_list_if_contains_any_substring(orglist,substrings):
    result = []
    for ele in orglist:
        contains = False
        for substr in substrings:
            if substr in ele: contains = True
        if not contains: result.append(ele)
    return result 

def insert_mystr_before_astr(orgstr,mystr,astr="?prune_day"):
    idx = orgstr.index(astr)
    return orgstr[:idx] + mystr + orgstr[idx:]

def grab_a_thread(url,n_pages = 30):
    post_entry_text = []
    page = 1
    title = ""
    while page <= n_pages:
        time.sleep(1)
        if page==1: page_url = url
        else: page_url = url + "page-" + str(page)
        fpage1 = requests.get(page_url)
        soup1 = BeautifulSoup(fpage1.content, 'html.parser')
        
        new_title = soup1.find_all('title')[0].get_text()
        if title == new_title: break
        else: title = new_title
        
        post_entry_contents = soup1.find_all(class_ = 'post entry-content ')
        for content in post_entry_contents:
            for parag in content.find_all('p'):
                post_entry_text.append(parag.get_text())
        page += 1
    return post_entry_text

def soup_a_thread(url,n_pages = 30, wait_time = 1):
    soups = []
    page = 1
    title = ""
    while page <= n_pages:
        time.sleep(wait_time)
        if page==1: page_url = url
        else: page_url = url + "page-" + str(page)
        fpage1 = requests.get(page_url)
        soup1 = BeautifulSoup(fpage1.content, 'html.parser')
        
        new_title = soup1.find_all('title')[0].get_text()
        if title == new_title: break
        else: title = new_title
        
        soups.append(soup1)
        page += 1
    return soups


def text_cleaning(string):
    string += "Edited by"
    string = string[:string.index("Edited by")].replace("\xa0","").replace("\n","").replace("\t","").replace("\r","")
    string = re.sub('\s+', ' ', string).strip()
    return string.replace(" .","").lstrip(".").lstrip(" ").rstrip().replace("...",".").replace("..",".")

def replace_urls(string):
    try:
        url_index = string.index("http")
        string_after = string[url_index:]+" "
        next_space_index = string_after.index(" ")
        string_after = replace_urls(string_after[next_space_index:])
        return (string[:url_index]+' URL '+ string_after).rstrip()
    except: return string

def has_image(post):
    return not post.find(class_ = 'resized_img')==None

def n_images(post):
    imgs = post.find_all(class_ = 'resized_img')
    if imgs == None: return 0
    else: return len(imgs)
    
def count_likes(like_text):
    if like_text == "": return 0
    elif not 'and' in like_text: return 1
    elif not ',' in like_text: return 2
    elif not 'other' in like_text: return 3
    else: 
        index = like_text.index(" other")
        return 3+int(like_text[index-2:index])

def n_likes(post):
    '''Input: beautiful soup object class post_body'''
    '''Output: number of likes to this post'''
    like_info = post.find(class_ = "ipsLikeBar_info")
    if  like_info == None: return 0
    else: 
        like_text = like_info.get_text().replace("\n","").replace("\t","")
        return count_likes(like_text)
    
def extract_title_from_thread_url(a_url):
    right_half = a_url[a_url.index("-")+1:-1].replace("-"," ")
    return right_half[:re.search("/|$", right_half).start()]

def emojis(post):
    '''Input: beautiful soup object class post_body'''
    '''Output: list of emojis as strings such as [':lol:','lol.gif']'''
    post_entry_content = post.find(class_="post entry-content ")
    content_list = list(post_entry_content.children)
    
    all_emojis = []
    for parts in content_list:
        if parts.name == 'blockquote': continue
        elif parts.name == 'img':
            try: 
                if parts['class'][0]=='bbc_emoticon': all_emojis.append(parts['alt'])
                elif parts['class'][0]=='bbc_img': all_emojis.append(parts['title'])
            except: pass
        else: 
            try: 
                for ele in parts.find_all(class_=re.compile('bbc_img'|'bbc_emot*')):
                    try: all_emojis.append(ele["title"]) 
                    except: 
                        try: all_emojis.append(ele["alt"]) 
                        except: pass
            except: pass
                    
    return all_emojis

def post_to_text(post):
    '''Input: beautiful soup object class post_body'''
    '''Output: cleaned post text'''
    post_entry_content = post.find(class_="post entry-content ")
    if type(post_entry_content) == type(None): post_entry_content = post.find(class_="post entry-content")
    content_list = list(post_entry_content.children)
    a_comment = ""
    for parts in content_list:
        if parts.name == 'p': a_comment+=". "+parts.get_text()
        elif type(parts) == bs4.element.NavigableString:a_comment+=". "+parts

    return replace_urls(text_cleaning(a_comment).lower())

def post_to_author_post_num(post_count_desc):
    '''Input: beautiful soup object class post_count desc lighter'''
    '''Output: the number of posts by the author'''
    return int(list(list(post_count_desc.children)[3].children)[0].replace('\n',''))


def all_info_from_a_souped_thread(a_souped_thread):
    all_info = []
    for page in a_souped_thread:
        posts = page.find_all(class_="post_body")
        author_post_counts = page.find_all(class_="post_count desc lighter")
        for i,post in enumerate(posts):
            n_author_posts = post_to_author_post_num(author_post_counts[i])
            n_i = n_images(post)
            text_record = text_cleaning(" ".join(emojis(post))+" "+ " ".join(["IMG"]*n_i)+". "+ post_to_text(post))
            all_info.append([text_record,n_likes(post),n_i,n_author_posts])
    return all_info

def nltk_sentiment(sentence):
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score