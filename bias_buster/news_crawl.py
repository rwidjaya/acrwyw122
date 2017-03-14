import bs4
import re
import json
from .util import get_strained_soup, get_soup

def extract(url, tag, attr):
	'''
	Extracts all URLS from a given news source homepage.
	Inputs:
		- url (str) = the url of the news source home page
		- tag (str) = the HTML tag that links are filed under in that url.
		- attr (dict) = attributes of above HTML tag.
	Output: links (list) = a list of url strings.
	'''
	soup = get_strained_soup(url,tag,attr)
	if tag=='a':
		stories = soup.findAll(href=True)
	else:
		stories = soup.findAll('a',href=True)
	links = []
	links = [a['href'] for a in stories if a['href'] not in links]
	return links

#NPR
def extract_npr():
	'''
	Finds and returns a list of all news urls from NPR.
	This includes the main news section and the breaking news section.
	Output: npr_links (list) = a list of url strings.
	'''
	npr_urls = ['http://www.npr.org/sections/news/', 'http://www.npr.org/sections/thetwo-way/']
	npr_tag = 'h2'
	npr_attr = {'class':'title'}
	'''npr_links1 = extract(npr_urls[0],npr_tag,npr_attr)
	npr_links2 = extract(npr_urls[1],npr_tag,npr_attr)
	npr_links = set(npr_links1 + npr_links2)
	return npr_links'''

	npr_links_clean = []
	for n in npr_urls:
		npr_links = extract(n,npr_tag,npr_attr)
		npr_links_clean += [a for a in npr_links if a not in npr_links_clean]
	return npr_links_clean

#WALL STREET JOURNAL
def extract_wsj():
	'''
	Finds and returns a list of all news urls from the Wall Street Journal homepage.
	Output: wsj_links_clean (list) = a list of url strings.
	'''
	wsj_url = 'https://www.wsj.com/'
	wsj_tag = 'a'
	wsj_attr = {'class':'wsj-headline-link'}
	wsj_links = extract(wsj_url,wsj_tag,wsj_attr)
	artrgx = re.compile(r'www.wsj.com')
	wsj_links_clean = [a for a in wsj_links if artrgx.search(a)]
	return wsj_links_clean

#FISCAL TIMES
def extract_tft():
	'''
	Finds and returns a list of all news urls from the Fiscal Times homepage.
	Output: tft_links_clean (list) = a list of url strings.
	'''
	tft_url = 'http://www.thefiscaltimes.com/'
	tft_tag = 'div'
	tft_attr = {'class':'view-content'}
	tft_links = extract(tft_url,tft_tag,tft_attr)
	artrgx = re.compile('\/\d{4}\/\d{2}\/\\d{2}')
	oprgx = re.compile('\/Columns\/|\/Media\/')
	tft_links_clean = ['http://www.thefiscaltimes.com'+a for a in tft_links \
		if artrgx.search(a) if not oprgx.search(a)]
	return tft_links_clean

#BREITBART
def extract_brt():
	'''
	Finds and returns a list of all news urls from the Breitbart homepage.
	Output: brt_links_clean (list) = a list of url strings.
	'''
	brt_url = 'http://www.breitbart.com/'
	brt_tag = 'h2'
	brt_attr = {'class' : 'title'}
	brt_links = extract(brt_url,brt_tag,brt_attr)
	brt_links_clean = ['http://www.breitbart.com'+a for a in brt_links]
	return brt_links_clean

#FOX NEWS
def extract_fox():
	'''
	Finds and returns a list of all news urls from Fox News.
	This includes the main homepage and the world news section.
	Output: fox_links (list) = a list of url strings.
	'''
	fox_hp = 'http://www.foxnews.com/'
	fox_soup = get_soup(fox_hp)
	fox_json = json.loads(fox_soup.find('script', type= 'application/ld+json').text)
	fox_links1 = []
	for j in fox_json['itemListElement']:
		foxrgx = re.compile(r'www.foxnews.com')
		fox_links1 += [l['url'] for l in j['item']['itemListElement'] \
			if foxrgx.search(l['url'])]

	fox_url = 'http://www.foxnews.com/world.html'
	fox_tag = 'h2'
	fox_links2 = extract(fox_url,fox_tag, None)
	oprgx = re.compile('\/opinion\/|sectionname')
	fox_links2_clean = ['http://www.foxnews.com'+a for a in fox_links2 \
		if not oprgx.search(a)]

	fox_links = list(set(fox_links1 + fox_links2_clean))
	return fox_links

#NEW YORK TIMES
def extract_nyt():
	'''
	Finds and returns a list of all news urls from the New York Times homepage.
	Output: nyt_links_clean (list) = a list of url strings.
	'''
	nyt_url = 'https://www.nytimes.com'
	nyt_tag = 'h2'
	nyt_attr = {'class' : 'story-heading'}
	nyt_links = extract(nyt_url,nyt_tag,nyt_attr)
	artrgx = re.compile(r'com'+'\/\d{4}\/\d{2}\/\\d{2}')
	oprgx = re.compile(r'opinion')
	nyt_links_clean = [a for a in nyt_links if artrgx.search(a) if not oprgx.search(a)]
	return nyt_links_clean

#MOTHER JONES
def extract_mojo():
	'''
	Finds and returns a list of all news urls from the Mother Jones homepage.
	Output: mojo_links_clean (list) = a list of url strings.
	'''
	mojo_url = 'http://www.motherjones.com/'
	mojo_tag = 'h3'
	mojo_attr = {'class':'title'}
	mojo_links = extract(mojo_url,mojo_tag,mojo_attr)
	mojo_links_clean = ['http://www.motherjones.com'+a for a in mojo_links]
	return mojo_links_clean

#HUFFINGTON POST
def extract_huff():
	'''
	Finds and returns a list of all news urls from the Huffington Post homepage.
	Output: huff_links_clean (list) = a list of url strings.
	'''
	huff_url = 'http://www.huffingtonpost.com/'
	huff_tag = 'a'
	huff_attr = {'class' : 'card__link'}
	huff_links = extract(huff_url,huff_tag,huff_attr)
	artrgx = re.compile(r'www.huffingtonpost.com')
	huff_links_clean = [a for a in huff_links if artrgx.search(a)]
	return huff_links_clean
