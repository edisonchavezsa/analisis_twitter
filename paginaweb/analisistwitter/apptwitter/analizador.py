# -*- coding: utf-8 -*-
from sklearn.externals import joblib
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from string import punctuation
from nltk.tokenize import word_tokenize

#import nltk
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    # remove non letters
    text = ''.join([c for c in text if c not in non_words])
    print("tokenizieaui"+str(text))
    # tokenize
    tokens = word_tokenize(text)

    # stem
    try:
        stems = stem_tokens(tokens, stemmer)
    except Exception as e:
        print(e)
        print(text)
        stems = ['']
    return stems

spanish_stopwords = stopwords.words('spanish')
non_words = list(punctuation)
non_words.extend([u'¿', u'¡'])
non_words.extend(map(str, range(10)))
stemmer = SnowballStemmer('spanish')
MICONSTANTE = joblib.load('/home/edisonchavezsa/Escritorio/Repositorios/python/Analisis_twitter/paginaweb/analisistwitter/corpus/estadiospipeline_nuevo_3.pkl')
print(MICONSTANTE)
