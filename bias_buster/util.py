from bs4 import SoupStrainer, BeautifulSoup
import urllib3
import numpy as np
import pandas as pd
import certifi
import re

allsides = pd.read_csv("./bias_buster/as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()

def get_soup(url):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    soup = BeautifulSoup(html, "lxml")
    return soup

def get_strained_soup(url, tag, attr=None):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    if attr:
        strained = SoupStrainer(tag, attrs=attr)
    else:
        strained = SoupStrainer(tag)
    return BeautifulSoup(html, "lxml", parse_only=strained)

def get_text(url):
    p_soup = get_strained_soup(url,'p')
    text = p_soup.find_all('p')
    txt = [t.text for t in text]
    return " ".join(txt)

def get_regex_url(url):
    urlrgx = re.compile('(https?:\/\/)?(www)\.([\da-z\.-]+)\.(com|net|org)')
    if urlrgx.search(url):
        urlstr = urlrgx.search(url).group(3)
        if urlstr in allsides.keys():
            return urlstr
    return False

def get_headline(url):
    h_soup = get_strained_soup(url, "title")
    tsep = "\||\:|\-"
    trgx = re.compile('(.*)\s'+tsep+'.*')
    headline = h_soup.text

    headline = trgx.search(headline).group(1)
    return headline
