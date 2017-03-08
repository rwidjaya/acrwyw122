import bs4
import re
import json
import pandas as pd
from newspaper import Article
import news_crawl as nc
import compare
import util
import mirror
from multiprocessing import Pool

allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()


def links_to_compare(url):
	is_featured = util.get_regex_url(url)

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
	news_links = [(url, link2) for link2 in news_links]
	return news_links

def get_story(url):
	if 'nytimes' in url:
		story_input = Article(url, keep_html_format = True)
		story_input.download()
		if story_input.is_downloaded:
			story_input.parse()
			story_text = story_input.text
	else:
		story_text = util.get_text(url)
	return story_text

def art_compare(url_tup):
	input_url, art_url = url_tup
	print(art_url)
	if util.get_regex_url(art_url):
		sim_score = compare.cossim(get_story(art_url), get_story(input_url))
		return (util.get_regex_url(art_url), art_url, sim_score)
	else:
		return None

def pop_bias(url):
	urls_to_crawl = links_to_compare(url)
	p = Pool(processes=20)
	compared = p.map_async(art_compare, urls_to_crawl).get()
	p.close()
	rv = {}

	for article in compared:
		if article:
			source, arturl, score = article
			info = allsides[source]
			news_name = info["Source Name"]
			news_bias = info["Bias"]
			print(score)
			if score > 0.3:
				if arturl not in rv:
					rv[news_name] = [news_bias, arturl, score]
				else:
					if rv[news_name][2] < sim_score:
						rv[news_name] = [news_bias, arturl, score]
					    #we want the article with highest sim score

	final_answer = {key: val[:2] for key, val in rv.items()}
	if len(final_answer) == 0:
		final_answer["none"] = ["Unfortunately, there were no comparable articles on sites with different biases.", ""]
	elif len(final_answer) < 3:
		num_articles = len(final_answer)
		final_answer["missing"] = ["We couldn't get 3 stories on the same topic for you.  But here's {}!".format(num_articles),""]

	return final_answer
