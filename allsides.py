import bs4
import urllib3
import csv
import numpy as np
import pandas as pd
import certifi
import util

asurl = "http://www.allsides.com/bias/bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&field_featured_bias_rating_value=1&title="

def source_info(soup):
    odd = soup.find_all("tr", class_="odd")
    odd = [(o, o.find_next("div", class_="rate-details")) for o in odd]
    even = soup.find_all("tr", class_="even")
    even = [(e, e.find_next("div", class_="rate-details")) for e in even]

    tags = [None]*(len(odd) + len(even))
    tags[::2] = odd
    tags[1::2] = even

    info = {}

    for t in tags:
        source = ""
        bias = ""
        agree = int(t[1].find("span", class_="agree").text)
        disagree = int(t[1].find("span", class_="disagree").text)
        alist = t[0].find_all("a", href=True)
        for a in alist:
            if "news-source" in a["href"]:
                source = a.text
            elif "bias" in a["href"]:
                rating = a.find("img")
                if rating:
                    bias = rating["alt"][6:]
        if source not in info:
            info[source] = (bias, agree, disagree, agree/disagree)

    return info

def go():
    soup = util.get_soup(asurl)
    info = source_info(soup)
    labels = ["News Source", "Bias", "Agree", "Disagree", "Ratio"]
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
    filename = "as.csv"
    go()
    print("\ncreated as.csv")
