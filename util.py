import bs4
from bs4 import SoupStrainer
import urllib3
import csv
import numpy as np
import pandas as pd
import certifi

def get_soup(url):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    soup = bs4.BeautifulSoup(html, "lxml")
    return soup

def get_strained_soup(url, tag, attr=None):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data

    if attr:
        strained = SoupStrainer(tag, attrs=attr)
    else:
        strained = SoupStrainer(tag)

    return bs4.BeautifulSoup(html, "lxml", parse_only=strained)

def get_text(url):
    p_soup = get_soup(url)
    text = p_soup.find_all("p")
    txt = [t.text for t in text]
    return " ".join(txt)
