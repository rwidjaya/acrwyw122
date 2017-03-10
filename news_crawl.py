import bs4
import re
import json
from util import get_strained_soup, get_soup


def extract(url, tag, attr):
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
	npr_urls = ['http://www.npr.org/sections/news/', 'http://www.npr.org/sections/thetwo-way/']
	npr_tag = 'h2'
	npr_attr = {'class':'title'}

	npr_links_clean = []
	
	for n in npr_urls:
		npr_links = extract(n,npr_tag,npr_attr)
		npr_links_clean += [a for a in npr_links if a not in npr_links_clean]

	return npr_links_clean


#WALL STREET JOURNAL
def extract_wsj():
	wsj_url = 'https://www.wsj.com/'
	wsj_tag = 'a'
	wsj_attr = {'class':'wsj-headline-link'}

	artrgx = re.compile(r'www.wsj.com')
	wsj_links = extract(wsj_url,wsj_tag,wsj_attr)
	wsj_links_clean = [a for a in wsj_links if artrgx.search(a)]

	return wsj_links_clean


#FISCAL TIMES
def extract_tft():
	tft_url = 'http://www.thefiscaltimes.com/'
	tft_tag = 'div'
	tft_attr = {'class':'view-content'}
	tft_links = extract(tft_url,tft_tag,tft_attr)

	artrgx = re.compile('\/\d{4}\/\d{2}\/\\d{2}')
	oprgx = re.compile('\/Columns\/|\/Media\/')
	tft_links_clean = ['http://www.thefiscaltimes.com/'+a for a in tft_links if artrgx.search(a) if not oprgx.search(a)]

	return tft_links_clean


#BREITBART
def extract_brt():
	brt_url = 'http://www.breitbart.com/'
	brt_tag = 'h2'
	brt_attr = {'class' : 'title'}
	brt_links = extract(brt_url,brt_tag,brt_attr)
	brt_links_clean = ['http://www.breitbart.com'+a for a in brt_links]

	return brt_links_clean


#FOX NEWS
def extract_fox():
	fox_hp = 'http://www.foxnews.com/'
	fox_soup = get_soup(fox_hp)
	fox_json = json.loads(fox_soup.find('script', type= 'application/ld+json').text)

	fox_links = []

	for j in fox_json['itemListElement']:
		for l in j['item']['itemListElement']:
			link = l['url']
			foxrgx = re.compile(r'www.foxnews.com')
			if (foxrgx.search(link)) and (link not in fox_links):
				fox_links += link

	fox_url = 'http://www.foxnews.com/world.html'
	fox_tag = 'h2'
	fox_add_links = extract(fox_url,fox_tag, None)
	
	oprgx = re.compile('\/opinion\/|sectionname')
	fox_add_links_clean = ['http://www.foxnews.com'+a for a in fox_add_links if not oprgx.search(a)]
	fox_links += fox_add_links_clean

	return fox_links


#NEW YORK TIMES
def extract_nyt():
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
	mojo_url = 'http://www.motherjones.com/'
	mojo_tag = 'h3'
	mojo_attr = {'class':'title'}
	mojo_links = extract(mojo_url,mojo_tag,mojo_attr)
	mojo_links_clean = ['http://www.motherjones.com'+a for a in mojo_links]

	return mojo_links_clean

#HUFFINGTON POST
def extract_huff():
	huff_url = 'http://www.huffingtonpost.com/'
	huff_tag = 'a'
	huff_attr = {'class' : 'card__link'}
	huff_links = extract(huff_url,huff_tag,huff_attr)

	artrgx = re.compile(r'www.huffingtonpost.com')
	huff_links_clean = [a for a in huff_links if artrgx.search(a)]

	return huff_links_clean
