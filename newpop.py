import bs4
import re
import json
import pandas as pd
import news_crawl as nc
import compare
from util import get_regex_url, get_story_or_title
import mirror
from multiprocessing import Pool

allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()
story = 0
title = 1

def links_to_compare(url):
	is_featured = get_regex_url(url)

	assert is_featured, "The news source is not in our database; please enter another article from different news source."

	news_list = mirror.get_mirrors(is_featured)
	news_links = []

	for nsource in news_list:
		if nsource == 'npr':
			news_links += nc.extract_npr()
		elif nsource == "wsj":
			news_links += nc.extract_wsj()
		elif nsource == "thefiscaltimes":
			news_links += nc.extract_tft()
		elif nsource == "foxnews":
			news_links += nc.extract_fox()
		elif nsource == "breitbart":
			news_links += nc.extract_brt()
		elif nsource == "nytimes":
			news_links += nc.extract_nyt()
		elif nsource == "motherjones":
			news_links += nc.extract_mojo()
		elif nsource == "huffingtonpost":
			news_links += nc.extract_huff()
	inputstory = get_story_or_title(url, story)
	return [(inputstory, link2) for link2 in news_links]

def art_compare(url_tup):
	inputstory, art_url = url_tup
	exists = get_regex_url(art_url)
	if exists:
		txt = get_story_or_title(art_url,story)
		print("got txt")
		sim_score = compare.cossim(txt,inputstory)
		print("got sim")
		head = get_story_or_title(art_url,title)

		return (head, exists, art_url, sim_score)

def pop_bias(url):
	urls_to_crawl = links_to_compare(url)
	p = Pool(processes=25)
	compared = p.map_async(art_compare, urls_to_crawl).get()
	p.close()

	input_head = get_story_or_title(url, title)
	input_info = allsides[get_regex_url(url)]
	input_source = input_info["Source Name"]
	input_bias = input_info["Bias"]
	rv = {input_head:(input_source, input_bias, url)}

	for article in compared:
		if article:
			headline, sourcergx, arturl, score = article
			info = allsides[sourcergx]
			source = info["Source Name"]
			bias = info["Bias"]
			if score > 0.3:
				if headline not in rv:
					rv[headline] = (source, bias, arturl, score)
				else:
					if rv[headline][3] < sim_score:
						rv[headline] = (source, bias, arturl, score)
					    #we want the article with highest sim score

	final_answer = {key: val[:3] for key, val in rv.items()}
	if len(final_answer) == 0:
		final_answer["none"] = \
		["Unfortunately, there were no comparable articles on sites with different biases.", ""]
	elif len(final_answer) < 4:
		num_articles = len(final_answer)
		final_answer["missing"] = \
		["We couldn't get 3 stories on the same topic for you.  But here's {}!".format(num_articles),""]

	return final_answer
