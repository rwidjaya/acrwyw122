import newspaper
import bs4
import re
import json
from util import get_soup, get_text

'''
NYT
'''

def extract_nyt(link):
	nyt_soup = get_soup(link)
	nyt_story = nyt_soup.findAll('h2', attrs={'class' : 'story-heading'})

	nyt_links = []

	for h2 in nyt_story:
		a = h2.find('a', href = True)
		if a:
			link = a['href']
			artrgx = re.compile(r'com'+'\/\d{4}\/\d{2}\/\\d{2}')
			oprgx = re.compile(r'opinion')
			if artrgx.search(link) and (not oprgx.search(link)) and (link not in nyt_links):
				nyt_links += [link]

	return nyt_links


'''
WSJ
'''

def extract_wsj(link):
	wsj_soup = get_soup(link)
	wsj_story = wsj_soup.findAll('a', attrs={'class' : 'wsj-headline-link'})

	wsj_links = []

	for a in wsj_story:
		link = a['href']
		artrgx = re.compile(r'www.wsj.com')
		if (artrgx.search(link)) and (link not in wsj_links):
			wsj_links += [link]

	return wsj_links


'''
BRT
'''

def extract_brt(link):
	brt_soup = get_soup(link)
	brt_story = brt_soup.findAll('h2', attrs={'class' : 'title'})

	brt_links = []

	for h2 in brt_story:
		a = h2.find('a', href = True)
		if a:
			link = a['href']
			if link not in brt_links:
				brt_links += ['http://www.breitbart.com'+link]

	return brt_links


'''
FOX
'''
def extract_fox(link):
	fox_soup = get_soup(link)
	fox_json = json.loads(fox_soup.find('script', type= 'application/ld+json').text)

	fox_links = []

	for j in fox_json['itemListElement']:
		for l in j['item']['itemListElement']:
			furl = l['url']
			foxrgx = re.compile(r'www.foxnews.com')
			if (foxrgx.search(furl)) and (link not in fox_news):
				fox_links += [furl]

	return fox_links


'''
MJS
'''
def extract_mjs(link):
	mjs_soup = get_soup(link)
	mjs_story = mjs_soup.findAll('h3', attrs={'class':'title'})

	mjs_links = []

	for h3 in mjs_story:
		a = h3.find('a', href = True)
		if a:
			link = a['href']
			if link not in mjs_links:
				mjs_links += ['http://www.motherjones.com'+link]

	return mjs_links


'''
HUF
'''
def extract_huf(link):
	huf_soup = get_soup(link)
	huf_story = huf_soup.findAll('a', attrs={'class' : 'card__link'})

	huf_links = []

	for a in huf_story:
		link = a['href']
		artrgx = re.compile(r'www.huffingtonpost.com')
		if (artrgx.search(link)) and (link not in huf_links):
			huf_links += [link]

	return huf_links

