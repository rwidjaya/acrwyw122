import bs4
import urllib3
import csv
import numpy as np
import pandas as pd
import certifi
import re
from .util import get_soup

asurl = "http://www.allsides.com/bias/bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&field_featured_bias_rating_value=1&title="

def get_source_url(url):
    '''
    Returns the source name tag of a news source on the AllSides bias ratings page.
    Input: url (str).
    Output: urlkey (str) = source name tag retrieved with regex.
    '''
    urlsoup = get_soup(url)
    urltag = urlsoup.find("div", class_="source-image")
    url = urltag.find("a")["href"].strip()
    urlkey = re.search(r"(?<=://)(www[.])?(.+)([a-z/]*\.[a-z/]*)", url)
    urlkey = urlkey.group(2).lower()
    return urlkey

def source_info(soup):
    '''
    Creates a dictionary of news sources, with values on bias rating, url, and
    the community agree/disagree ratio on the respective bias ratings.
    Input: soup (BeautifulSoup object) = soup of the AllSides bias ratings page.
    Outpu: info (dict of tuples) = dictionary of news source information.
    '''
    odd = soup.find_all("tr", class_="odd")
    odd = [(o, o.find_next("div", class_="rate-details")) for o in odd]
    even = soup.find_all("tr", class_="even")
    even = [(e, e.find_next("div", class_="rate-details")) for e in even]
    tags = [None]*(len(odd) + len(even))
    tags[::2] = odd
    tags[1::2] = even

    info = {}

    for t in tags:
        url = ""
        source = ""
        bias = ""
        agree = int(t[1].find("span", class_="agree").text)
        disagree = int(t[1].find("span", class_="disagree").text)
        alist = t[0].find_all("a", href=True)
        for a in alist:
            if "news-source" in a["href"]:
                if "how-do-we-fix-it" in a["href"]:
                    url = "howdowefixit"
                elif "media-matters" in a["href"]:
                    url = "mediamatters"
                elif "media-research-center" in a["href"]:
                    url = "mrc"
                elif "newsweek" in a["href"]:
                    url = "newsweek"
                elif "slate" in a["href"]:
                    url = "slate"
                elif "hill" in a["href"]:
                    url = "thehill"
                elif "reason" in a["href"]:
                    url = "reason"
                elif "watchdogorg" in a["href"]:
                    url = "watchdog"
                elif "wall-street-journal" in a["href"]:
                    url = "wsj"
                else:
                    url = get_source_url("www.allsides.com{}".format(a["href"]))
                source = a.text
            elif "bias" in a["href"]:
                rating = a.find("img")
                if rating:
                    bias = rating["alt"][6:]
        if url not in info:
            info[url] = (source, bias, agree, disagree, agree/disagree)

    return info

def go():
    '''
    Prints the source info as a pandas dataframe and writes to a csv.
    '''
    soup = get_soup(asurl)
    info = source_info(soup)
    labels = ["News Source URL", "Source Name", "Bias", "Agree", "Disagree", "Ratio"]
    df = pd.DataFrame(info, index=labels[1:]).T
    df.columns.name = "News Source"
    print(df)

    with open("as.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(labels)
        for key in sorted(info.keys()):
            row = [key]
            row += [val for val in info[key]]
            writer.writerow(row)


if __name__ == "__main__":
    go()
    print("\ncreated as.csv")
