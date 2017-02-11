import util
import nltk
#nltk.download("punkt") download once if you haven't yet
from nltk.corpus import brown
import string
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = nltk.stem.porter.PorterStemmer()
nopunc = dict((ord(p), None) for p in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def clean(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(nopunc)))

sw = brown.words(categories='news') + brown.words(categories='editorial') + brown.words(categories='reviews')
v = TfidfVectorizer(tokenizer=clean, stop_words=sw)

def cossim(article1, article2):
    tfidf = v.fit_transform([article1, article2])
    return ((tfidf * tfidf.T).A)[0,1]


g = "https://www.theguardian.com/us-news/2017/feb/09/judges-deny-trump-travel-ban-enforcement-uphold-order"
b = "http://www.breitbart.com/big-government/2017/02/10/nuclear-option-trump-exec-order-sets-showdown-executive-judicial-branches/"
guardian = util.get_text(g)
breitbart = util.get_text(b)

print("cosine similarity: {}".format(cossim(guardian, breitbart)))#
