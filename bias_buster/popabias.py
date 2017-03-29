import pandas as pd
from .news_crawl import *
from .compare import cossim
from .util import get_regex_url, get_storytitle
from .mirror import get_mirrors
from multiprocessing import Pool

allsides = pd.read_csv("./bias_buster/as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()

def links_to_compare(url):
    '''
    Generates a list of potential urls to suggest to user from mirror-rank sources.
    Input: url (str) = the link to a news article given by the user.
    Output: list of tuples - (input headline (str), input story text (str), url to compare (str))
    '''
    is_featured = get_regex_url(url)
    assert is_featured, "The news source is not in our database; please enter another article from different news source."

    news_list = get_mirrors(is_featured)
    news_links = []

    for nsource in news_list:
        if nsource == "npr":
            news_links += extract_npr()
        elif nsource == "wsj":
            news_links += extract_wsj()
        elif nsource == "thefiscaltimes":
            news_links += extract_tft()
        elif nsource == "foxnews":
            news_links += extract_fox()
        elif nsource == "breitbart":
            news_links += extract_brt()
        elif nsource == "nytimes":
            news_links += extract_nyt()
        elif nsource == "motherjones":
            news_links += extract_mojo()
        elif nsource == "huffingtonpost":
            news_links += extract_huff()

    input_head, input_text = get_storytitle(url)
    return [(input_head, input_text, link2) for link2 in news_links]
    #Getting the text and title of the original url here avoids pulling NYT and Fiscal Times urls more than once.
    #Calling NYT and Fiscal Times more than once results in a max retries error.
    #Additionally, Pool.map_async only takes one argument, while we need to compare the text of two articles.
    #Containing this in a tuple was the best way of packaging multiple arguments into one.

def art_compare(comparison_tup):
    '''
    Compares two articles for cosine similarity and returns their score and the
    headline, source name tag, and url of the non-user-inputted article.
    Input: comparison_tup = (input headline (str), input text (str), article url (str))
    Output: tuple of headline, source name tag, and url of the non-user-inputted
        article, along with its cosine similarity with the user-inputted url.
    '''
    input_head, input_text, art_url = comparison_tup
    #if 'npr' in art_url:
    #    exists = 'npr'
    #else:
    exists = get_regex_url(art_url)
    if exists:
        head, txt = get_storytitle(art_url)
        sim_score = cossim(txt,input_text)
        return (head, exists, art_url, sim_score)

def pop_bias(url):
    '''
    Checks the bias rating of a user-inputted url.
    Returns a dictionary of news headlines from mirror-ranked sources, with
    values of the articles' bias ratings and urls.
    Input: url (str)
    Output: final_answer (dict) = dict of headline strings with tuple values
        containing a bias rating (str) and article url (str).
    '''
    urls_to_crawl = links_to_compare(url)
    p = Pool(processes=25)
    compared = p.map_async(art_compare, urls_to_crawl).get()
    p.close()

    input_head, input_text = get_storytitle(url)
    input_info = allsides[get_regex_url(url)]
    input_source = input_info["Source Name"]
    input_bias = input_info["Bias"]
    #rv = {input_source:(input_head, input_bias, url, 1)}
    rv = {}

    for article in compared:
        if article:
            headline, sourcergx, arturl, score = article
            info = allsides[sourcergx]
            source = info["Source Name"]
            bias = info["Bias"]
            if score > 0.3:
                if source not in rv:
                    rv[source] = (headline, bias, arturl, score)
                else:
                    if rv[source][3] < score:
                        rv[source] = (headline, bias, arturl, score)
					    #We want the article with highest similarity score.

    final_answer = {val[0]: (val[1], val[2], key) for key, val in rv.items()}
    if len(final_answer) == 0:
        final_answer["none"] = \
        ("Unfortunately, there were no comparable articles on sites with different biases.","")
    elif len(final_answer) < 4:
        num_articles = len(final_answer) 
        final_answer["missing"] = \
        ("We couldn't get 3 stories on the same topic for you.  But here's {}!".format(num_articles),"")

    return (final_answer, input_bias)
