import pandas as pd
import numpy as np
import random

allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL")
ranks = ["Left", "Lean Left", "Center", "Lean Right", "Right"]
ranksrev = ranks[::-1]
sites = ["npr", "wsj", "thefiscaltimes", "foxnews", "breitbart", "nytimes", "motherjones", "huffingtonpost"]

def get_mirrors(url):
    #where url = the regex cleaned portion of the url

    if url in allsides.index:
        opprank = ranksrev[ranks.index(allsides.ix[url, "Bias"])]
        murls = allsides.ix[sites]
        murls_rank = murls.Bias == opprank

        mirrors = murls[murls_rank].index
        mirrors = list(mirrors)

        #need to find better way to include the center leaning news
        mirrors += ["npr", "wsj"]

        if opprank == "Center":
            mirrors += [random.choice["huffingtonpost","motherjones", "nytimes"]]
            mirrors += [random.choice["foxnews","breitbart","thefiscaltimes"]]

        if url in mirrors:
        	mirrors.remove(url)

        return mirrors
