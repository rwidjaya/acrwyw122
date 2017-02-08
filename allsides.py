import bs4
import urllib3

def get_soup(url):
    '''
    Generates a BeautifulSoup object given a URL.
    Input: url (string)
    Returns: BeautifulSoup object
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data
    return bs4.BeautifulSoup(html, "html5lib")

def source_info(soup):
    odd = soup.find_all("tr", class_="odd")
    odd = [(o, o.find_next("div", class_="rate-details")) for o in odd]
    even = soup.find_all("tr", class_="even")
    even = [(e, e.find_next("div", class_="rate-details")) for e in even]

    tags = [None]*(len(odd) + len(even))
    tags[::2] = odd
    tags[1::2] = even

    info = []

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
        info += [(source, bias, agree, disagree, agree/disagree)]

    return info

"""
<td class="views-field views-field-title source-title">
<td class="views-field views-field-field-bias-image">
<a href="/bias/right-center">
<span class="agree">
<span class="disagree">
http://www.allsides.com/bias/bias-ratings?field_news_source_type_tid=2&field_news_bias_nid=1&field_featured_bias_rating_value=1&title=
"""
