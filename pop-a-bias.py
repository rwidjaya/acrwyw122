import bs4
import re
import json
#from newspaper import Article
from news_crawl import *
from allsides import *
from util import *
from mirror import *


asoup = get_soup(asurl)
allsides = source_info(asoup)

def in_allsides(link):
	urlrgx = re.compile('(https?:\/\/)?(www)\.([\da-z\.-]+)\.(com|net|org|com)')
	urlstr = urlrgx.search(link).group(3)

	if urlstr in allsides.keys():
		return urlstr

	return False


def pop_bias(link):
	is_featured = in_allsides(link)

	assert is_featured, "The news source is not in our database, please enter another article from different news source."

	news_list = get_mirror(is_featured)
	rv = {}

	'''story_input = Article(link, keep_html_format = True)
	story_input.download()
	story_input.parse()
	story_input.nlp()

	story_input_keywords = story_input.keywords
	story_input_text = story_input.text'''

	story_input_text = get_text(link)

	for nsource in news_list:
		if nsource == 'npr':
			news_links = extract_npr()

		elif nsource == "wsj":
			news_links = extract_wsj()

		elif nsource == "thefiscaltimes":
			news_links = extract_fnt()

		elif nsource == "foxnews":
			news_links = extract_fox()

		elif nsource == "breitbart":
			news_links = extract_brt()

		elif nsource == "nytimes":
			news_links = extract_nyt()

		elif nsource == "motherjones":
			news_links = extract_mjs()

		elif nsource == "huffingtonpost":
			news_links = extract_huf()

		news_name, news_bias, agree, disagree, ratio = allsides[n]

		sim_score = 0
		sim_article = ""

		for narticle in news_links:
			'''story = Article(n, keep_html_format = True)
			story.download()
			story.parse()
			story.nlp()

			story_keywords = story.keywords
			story_text = story.textst'''
			story_text = get_text(narticle)

			sim_score = cossim(story_input_text, story_text)

			if sim_score > 0.3:
				if narticle not in rv:
					rv[news_name] = [news_bias, narticle, cossim]
				else:
					if rv[news_name][2] < sim_score:
						rv[news_name] = [nsource, narticle, cossim]
						#we want the article with highest sim score

	final_answer = {key: val[:2] for key, val in rv.items()}

	return final_answer
