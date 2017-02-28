import pandas as pd
import numpy as np

allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL")
ranks = ["Left", "Lean Left", "Centre", "Lean Right", "Right"]
ranksrev = ranks[::-1]

def get_mirrors(url):

    if url in allsides.index:
        opprank = ranksrev[ranks.index(allsides.ix[url, "Bias"])]
        print(opprank)
        murls = allsides["Bias"] == opprank
        mirrors = allsides[murls].index

        return list(mirrors)
