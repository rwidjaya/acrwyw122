import newspaper
import bs4
import re
import json
from util import get_soup, get_text

'''
NPR
'''
def extract_npr():
	npr_url = 'http://www.npr.org/sections/news/'
	npr_soup = get_soup(npr_url)
	npr_story = npr_soup.findAll('h2', attrs={'class':'title'})

	npr_links = []

	for h2 in npr_story:
		a = h2.find('a', href = True)
		if a:
			link = a['href']
			if link not in npr_links:
			# if (artrgx.search(link)) and (not oprgx.search(link)) and (link not in npr_links):
				npr_links += [link]
	return npr_links


'''
WSJ
'''
def extract_wsj():
	wsj_url = 'https://www.wsj.com/'
	wsj_soup = get_soup(wsj_url)
	wsj_story = wsj_soup.findAll('a', attrs={'class' : 'wsj-headline-link'})

	wsj_links = []

	for a in wsj_story:
		link = a['href']
		artrgx = re.compile(r'www.wsj.com')
		if (artrgx.search(link)) and (link not in wsj_links):
			wsj_links += [link]

	return wsj_links


'''
FNT
'''
def extract_fnt():
	fnt_url = 'http://www.thefiscaltimes.com/'
	fnt_soup = get_soup(fnt_url)
	fnt_story = fnt_soup.findAll('div', attrs={'class':'view-content'})

	fnt_links = []

	for div in fnt_story:
		a = div.findAll('a', href = True)

		for href in a:
			link = href['href']
			artrgx = re.compile('\/\d{4}\/\d{2}\/\\d{2}')
			oprgx = re.compile('\/Columns\/|\/Media\/')

			if (artrgx.search(link)) and (not oprgx.search(link)) and (link not in fnt_links):
				fnt_links += ['http://www.thefiscaltimes.com/'+link]

	return fnt_links

'''
BRT
'''

def extract_brt():
	brt_url = 'http://www.breitbart.com/'
	brt_soup = get_soup(brt_url)
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
def extract_fox():
	fox_url = 'http://www.foxnews.com/'
	fox_soup = get_soup(fox_url)
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
BSG

def extract_bsg():
	bsg_url = 'http://www.bostonglobe.com/'
	bsg_soup = get_soup(bsg_url)
	bsg_story = bsg_soup.findAll('div', attrs={'class':'story'})

	bsg_links = []

	for div in bsg_story:
		a = div.find('a', href = True)
		if a:
			link = a['href']
			artrgx = re.compile(r'http')
			oprgx = re.compile(r'opinion')
			if (not artrgx.search(link)) and (not oprgx.search(link)) and (link not in bsg_links):
				bsg_links += ['https://www.bostonglobe.com'+link]

	return bsg_links
'''

'''
NYT
'''

def extract_nyt():
	nyt_url = 'https://www.nytimes.com'
	nyt_soup = get_soup(nyt_url)
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
MJS
'''
def extract_mjs():
	mjs_url = 'http://www.motherjones.com/'
	mjs_soup = get_soup(mjs_url)
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
def extract_huf():
	huf_url = 'http://www.huffingtonpost.com/'
	huf_soup = get_soup(huf_url)
	huf_story = huf_soup.findAll('a', attrs={'class' : 'card__link'})

	huf_links = []

	for a in huf_story:
		link = a['href']
		artrgx = re.compile(r'www.huffingtonpost.com')
		if (artrgx.search(link)) and (link not in huf_links):
			huf_links += [link]

	return huf_links
