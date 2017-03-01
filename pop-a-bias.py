import bs4
import re
import json
from newspaper import Article
from news_crawl import *
from allsides import *
from util import *
from mirror import *


assoup = get_soup(asurl)
info = source_info(assoup)

def in_allsides(link):
	urlrgx = re.compile('(https?:\/\/)?(www)\.([\da-z\.-]+)\.(com|net|org|com)')
	urlstr = urlrgx.search(link).group(3)
	
	if urlstr in info.keys():
		return urlstr
	
	return False


def pop_bias(link):
	is_featured = in_allsides(link)

	assert is_featured, "The news source is not in our database, please enter another article from different news source."

	news_list = get_mirror(is_featured)
	rv = {}

	story_input = Article(link, keep_html_format = True)
	story_input.download()
	story_input.parse()
	story_input.nlp()

	story_input_keywords = story_input.keywords
	story_input_text = story_input.text

	for n in news_list:
		if n == 'npr':
			news_links = extract_npr()
		
		elif n == "wsj":
			news_links = extract_wsj()

		elif n == "thefiscaltimes":
			news_links = extract_fnt()

		elif n == "foxnews":
			news_links = extract_fox()

		elif n == "breitbart":
			news_links = extract_brt()

		elif n == "nytimes":
			news_links = extract_nyt()

		elif n == "motherjones":
			news_links = extract_mjs()

		elif n == "huffingtonpost":
			news_links = extract_huf()

		news_name, news_bias, agree, disagree, ratio = info[n]

		sim_score = 0
		
		for n in news_links:
			story = Article(n, keep_html_format = True)
			story.download()
			story.parse()
			story.nlp()

			story_keywords = story.keywords
			story_text = story.text

			sim_score = cossim(story_input_text, story_text)

			#consider: using article keyword for preilminary sorting?
			#??? WHAT IS THE SCORING MECHANISM???

	return {}







	


	







