import bs4
import re
import json
import pandas as pd
from newspaper import Article
import news_crawl as nc
import compare
import util
import mirror


allsides = pd.read_csv("as.csv")
allsides = allsides.set_index("News Source URL").T.to_dict()

def in_allsides(link):
	urlrgx = re.compile('(https?:\/\/)?(www)\.([\da-z\.-]+)\.(com|net|org)')
	urlstr = urlrgx.search(link).group(3)

	if urlstr in allsides.keys():
		return urlstr

	return False


def pop_bias(link):
	is_featured = in_allsides(link)

	assert is_featured, "The news source is not in our database, please enter another article from different news source."

	news_list = mirror.get_mirrors(is_featured)
	rv = {}

	print(news_list)

	story_input = Article(link, keep_html_format = True)
	story_input.download()
	if story_input.is_downloaded:
		story_input.parse()
		story_input_text = story_input.text
	else:
		story_text = util.get_text(link)

	for nsource in news_list:
		if nsource == 'npr':
			news_links = nc.extract_npr()

		elif nsource == "wsj":
			news_links = nc.extract_wsj()

		elif nsource == "thefiscaltimes":
			news_links = nc.extract_fnt()

		elif nsource == "foxnews":
			news_links = nc.extract_fox()

		elif nsource == "breitbart":
			news_links = nc.extract_brt()

		elif nsource == "nytimes":
			news_links = nc.extract_nyt()

		elif nsource == "motherjones":
			news_links = nc.extract_mjs()

		elif nsource == "huffingtonpost":
			news_links = nc.extract_huf()

		info = allsides[nsource]
		news_name = info["Source Name"]
		news_bias = info["Bias"]
		agree = info["Agree"]
		disagree = info["Disagree"]
		ratio = info["Ratio"]

		sim_score = 0
		sim_article = ""

		for narticle in news_links:
			story = Article(narticle, keep_html_format = True)
			story.download()
			if story.is_downloaded:
				story.parse()
				story_text = story.text
			else:
				story_text = util.get_text(narticle)

			sim_score = compare.cossim(story_input_text, story_text)
			if sim_score > 0.3:
				if narticle not in rv:
					rv[news_name] = [news_bias, narticle, sim_score]
				else:
					if rv[news_name][2] < sim_score:
						rv[news_name] = [nsource, narticle, sim_score]
						#we want the article with highest sim score

	final_answer = {key: val[:2] for key, val in rv.items()}
	if len(final_answer) == 0:
		final_answer["none"] = ["Unfortunately, there were no comparable articles on sites with different biases.", ""]
	elif len(final_answer) < 3:
		num_articles = len(final_answer)
		final_answer["missing"] = ["We couldn't get three other stories on the same topic for you.  But here's {} articles!".format(num_articles),""]

	return final_answer
