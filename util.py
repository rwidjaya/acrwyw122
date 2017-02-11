import bs4
import urllib3
import csv
import numpy as np
import pandas as pd
import certifi

def get_soup(url):
    pm = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    html = pm.urlopen(url=url, method="GET").data
    soup = bs4.BeautifulSoup(html, "html5lib")
    return soup

def get_text(url):
    soup = get_soup(url)
    text = soup.find_all("title") + soup.find_all("h1") + soup.find_all("p")
    txt = [t.text for t in text]
    return " ".join(txt)
