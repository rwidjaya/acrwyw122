import pandas as pd
import random

allsides = pd.read_csv("./bias_buster/as.csv")
allsides = allsides.set_index("News Source URL")
ranks = ["Left", "Lean Left", "Center", "Lean Right", "Right"]
ranksrev = ranks[::-1]
sites = ["npr", "wsj", "thefiscaltimes", "foxnews", "breitbart", "nytimes", "motherjones", "huffingtonpost"]

def get_mirrors(url):
    '''
    Returns 2 centrist and 1 opposite-leaning news source if url is biased.
    Returns 2 centrist, 1 left, and 1 right-leaning news source if url is centrist but not WSJ or NPR.
    Returns 1 centrist, 1 left, and 1 right-leaning news source if url is WSJ or NPR.
    Input: url (str) = the source name tag cleaned portion of a given news article url.
    Output: list of mirror url strings
    '''
    mirrors = []
    if url in allsides.index:
        opprank = ranksrev[ranks.index(allsides.ix[url, "Bias"])]
        murls = allsides.ix[sites]
        murls_rank = murls.Bias == opprank

        mirrors = murls[murls_rank].index
        mirrors = list(mirrors)

        if url == "wsj":
            mirrors += ["npr"]
        elif url == "npr":
            mirrors += ["wsj"]
        else:
            mirrors += ["npr", "wsj"]

        if opprank == "Center":
            mirrors += [random.choice(["huffingtonpost","motherjones", "nytimes"])]
            mirrors += [random.choice(["foxnews","breitbart","thefiscaltimes"])]

    if url in mirrors:
        mirrors.remove(url)
    return list(set(mirrors))
