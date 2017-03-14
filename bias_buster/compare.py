import nltk
#nltk.download("punkt") #download once if you haven't yet
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import csv

#stopwords = open('stopwords.txt','r')
#reader = csv.reader(stopwords)
#sw = set([row[0] for row in reader])
sw = set(stopwords.words('english'))

stemmer = nltk.stem.porter.PorterStemmer()
nopunc = dict((ord(p), None) for p in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def clean(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(nopunc)))


def cossim(article1, article2):
    '''
    Creates and standardises tfidf vector.
    Returns cosine similarity score of two articles.
    Inputs: article1 (str), article2 (str).
    Output: cosine_similarity score (float).
    '''
    v = TfidfVectorizer(tokenizer=clean, stop_words=sw)
    tfidf = v.fit_transform([article1, article2])
    return cosine_similarity(tfidf[0], tfidf[1])[0,0]

'''
#Sample Usage:
g = 'https://www.theguardian.com/us-news/2017/mar/13/budget-office-republican-healthcare-coverage-deficit-costs'
b = 'http://www.breitbart.com/big-government/2017/03/13/cbo-report-ryan-plan-drops-number-of-insured-24-million-by-2026/'
import util
guardian = util.get_story(g)
breitbart = util.get_story(b)
print(guardian)
print("cosine similarity: {}".format(cossim(guardian, breitbart)))
#cossim(guardian, breitbart)
'''
