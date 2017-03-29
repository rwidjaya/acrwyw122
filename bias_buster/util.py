'''
Contains all helper functions related to parsing url strings and BeautifulSoup objects
or retrieving text from a url string.
'''

from bs4 import SoupStrainer, BeautifulSoup
import urllib3
import numpy as np
import pandas as pd
import certifi
import re
from newspaper import Article


allsides = pd.read_csv("./bias_buster/as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()

def get_soup(url):
    '''
    Returns BeautifulSoup object of a given url.
    Input: url (str).
    Output: BeautifulSoup object.
    '''
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    return BeautifulSoup(html, "lxml")

def get_strained_soup(url, tag, attr=None):
    '''
    Returns a filtered BeautifulSoup object with SoupStrainer.
    Inputs:
        - url (str).
		- tag (str) = HTML tag that user wishes to retrieve.
		- attr (dict) = attributes of above HTML tag.
    Output: strained BeautifulSoup object.
    '''
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    if attr:
        strained = SoupStrainer(tag, attrs=attr)
    else:
        strained = SoupStrainer(tag)
    return BeautifulSoup(html, "lxml", parse_only=strained)

def get_regex_url(url):
    '''
    Returns the source name tag of a news source url.
    Input: url (str).
    Output: urlstr (str) = source name tag retrieved with regex.
    '''
    urlrgx = re.compile(r"(?<=://)(www[\.])?(.*)(\.com|\.org|\.net)(.*)")
    if urlrgx.search(url):
        urlstr = urlrgx.search(url).group(2)
        if urlstr in allsides.keys():
            return urlstr

def get_Article(url):
    '''
    Retrieves article information for New York Times and Fiscal Times.
    Input: url (str).
    Output: tuple of article headline (str), article text (str).
    '''
    if ('nyt' in url) or ('fiscaltimes'in url):
        art = Article(url, keep_html_format = True)
        art.download()
        if art.is_downloaded:
            art.parse()
            return (art.title, art.text)

def get_headline(url):
    '''
    Retrieves headline text of an article url.
    Input: url (str).
    Output: headline string.
    '''
    h_soup = get_strained_soup(url, "title")
    trgx ='(.*)\s(?=\:|\-|\|)'
    headline = h_soup.text
    t = re.compile(trgx)
    if t.search(headline):
        return t.search(headline).group(1).strip()

def get_story(url):
    '''
    Retrieves story text of an article url.
    Input: url (str).
    Output: story string.
    '''
    p_soup = get_strained_soup(url,'p')
    text = p_soup.find_all('p')
    txt = [t.text for t in text]
    return " ".join(txt)

def get_storytitle(url):
    '''
    Retrieves headline text and story text of an article url.
    Input: url (str).
    Output: story_tup = (headline string, story string)
    '''
    story_tup = get_Article(url)
    if not story_tup:
        text = get_story(url)
        title = get_headline(url)
        story_tup = (title, text)
    return story_tup
