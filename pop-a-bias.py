import bs4
import newspaper
import bs4
import re
import json
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

	for n in news_list:
		if n == 'npr':
			news_links = extract_npr()
			news_name, news_bias, agree, disagree, ratio = info[n]

			nltk_score = 0
			#loop through each url in news_links
				#use newspaper to extract article text (bc NYT cannot be extracted using get_text)/modify get_text --> roadblock atm
				#run it through compare.py, store result
				#consider using article keyword for preilminary sorting?
				#??? WHAT IS THE CHOICE MECHANISM???

			#update dict with name, bias, and comparable url 



		elif n == "wsj":
			news_links = extract_wsj()
			news_name, news_bias, agree, disagree, ratio = info[n]


		elif n == "thefiscaltimes":
			news_links = extract_fnt()
			news_name, news_bias, agree, disagree, ratio = info[n]

		elif n == "foxnews":
			news_links = extract_fox()
			news_name, news_bias, agree, disagree, ratio = info[n]

		elif n == "breitbart":
			news_links = extract_brt()
			news_name, news_bias, agree, disagree, ratio = info[n]

		elif n == "nytimes":
			news_links = extract_nyt()
			news_name, news_bias, agree, disagree, ratio = info[n]

		elif n == "motherjones":
			news_links = extract_mjs()
			news_name, news_bias, agree, disagree, ratio = info[n]

		elif n == "huffingtonpost":
			news_links = extract_huf()
			news_name, news_bias, agree, disagree, ratio = info[n]







	


	







