from bs4 import SoupStrainer, BeautifulSoup
import urllib3
import csv
import numpy as np
import pandas as pd
import certifi
import re
from newspaper import Article

allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()

def get_soup(url):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    return BeautifulSoup(html, "lxml")

def get_strained_soup(url, tag, attr=None):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    if attr:
        strained = SoupStrainer(tag, attrs=attr)
    else:
        strained = SoupStrainer(tag)
    return BeautifulSoup(html, "lxml", parse_only=strained)

def get_regex_url(url):
    urlrgx = re.compile('(https?:\/\/)?(www)\.([\da-z\.-]+)\.(com|net|org)')
    if urlrgx.search(url):
        urlstr = urlrgx.search(url).group(3)
        if urlstr in allsides.keys():
            return urlstr

def get_Article(url, storyortitle):
    if ('nytimes' in url) or ('fiscaltimes'in url):
        art = Article(url, keep_html_format = True)
        art.download()
        if art.is_downloaded:
            art.parse()
            if storyortitle == 0:
                return art.text

def get_headline(url):
    h_soup = get_strained_soup(url, "title")
    trgx = re.compile('(.*)(?=-)')
    headline = h_soup.text

    #headline = trgx.search(headline).group(0)
    return headline.strip()

def get_story(url):
    p_soup = get_strained_soup(url,'p')
    text = p_soup.find_all('p')
    txt = [t.text for t in text]
    return " ".join(txt)

def get_story_or_title(url, storyortitle):
    text = get_Article(url,storyortitle)
    if not text:
        if storyortitle == 0:
            text = get_story(url)
        elif storyortitle == 1:
            text = get_headline(url)
    return text
