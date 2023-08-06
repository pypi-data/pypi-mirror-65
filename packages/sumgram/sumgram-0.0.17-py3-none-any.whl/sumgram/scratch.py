import json
from sumgram.sumgram import get_top_sumgrams

from datetime import datetime
import os
import logging

from genericCommon import dumpJsonToFile
from genericCommon import readTextFromFile
from genericCommon import getStopwordsSet
from sklearn.feature_extraction.text import CountVectorizer


def get_red_txt(txt):
	return "\033[91m{}\033[00m" .format(txt)

def testSumgram():
	ngram = 2
	params = {
		'top_ngram_count': 20,
		'ngram_printing_mw': 60,
		'title': '*TITLE*'
	}

	doc_List = [
		{'idu': 'x', 'text': 'The eye of Category 4 Hurricane Harvey is now over Aransas Bay. A station at Aransas Pass run by the Texas Coastal Observing Network recently reported a sustained wind of 102 mph with a gust to 132 mph. A station at Aransas Wildlife Refuge run by the Texas Coastal Observing Network recently reported a sustained wind of 75 mph with a gust to 99 mph. A station at Rockport reported a pressure of 945 mb on the western side of the eye.'},
		{'idu': 'y', 'text': 'Eye of Category 4 Hurricane Harvey is almost onshore. A station at Aransas Pass run by the Texas Coastal Observing Network recently reported a sustained wind of 102 mph with a gust to 120 mph.'},
		{'idu': 'z', 'text': 'Hurricane Harvey has become a Category 4 storm with maximum sustained winds of 130 mph. Sustained hurricane-force winds are spreading onto the middle Texas coast.'}
	]

	sumgrams = get_top_sumgrams(doc_List, ngram, params=params)
	with open('sumgrams.json', 'w') as outfile:
		json.dump(sumgrams, outfile)

def getData():
	
	print('\ngetData():')

	#rp = '/Users/renaissanceassembly/Documents/tmp/NgramSumTst/cols/plaintext/trump/trump-tweets/'
	rp = '/Users/renaissanceassembly/Documents/tmp/NgramSumTst/cols/plaintext/trump/trump-tweets/'
	files = os.listdir(rp)
	doc_lst = []

	for f in files:
		
		infile = open(rp + f, 'r')
		doc_lst.append(infile)
		

	return doc_lst

def testFitTransform(doc_lst):
	
	print('\ntestFitTransform():')

	count_vectorizer = CountVectorizer(stop_words=getStopwordsSet(), token_pattern=r'(?u)\b[a-zA-Z\'\’-]+[a-zA-Z]+\b|\d+[.,]?\d*', ngram_range=(2, 2), binary=True)
	#tf_matrix is a binary TF matrix if doc_lst.len > 1, non-binary otherwise
	tf_matrix = count_vectorizer.fit_transform(doc_lst).toarray()

	#every entry in list top_ngrams is of type: (a, b), a: term, b: term position in TF matrix
	top_ngrams = count_vectorizer.get_feature_names()

testSumgram()
