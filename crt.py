import requests, string, unicodedata
from string import punctuation
from string import maketrans
from time import time
#
import json
import simplejson
from simplejson.scanner import errmsg
#
import nltk
from nltk import pos_tag,word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer


# Oxford Dictionary API keys
# Get API Credentials here -> https://developer.oxforddictionaries.com
app_id = '********'
app_key = '***********************'
address = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'

with open("webster_dictionary.txt") as f:
	en_dictionary = f.read().splitlines()

def get_stopwords(language='english'):
	return set(stopwords.words(language))

def remove_punc(sentence):	
	no_punc = lambda s: s.translate(string.maketrans("",""), string.punctuation)
	try:
		op = no_punc(sentence.encode('utf-8'))
	except UnicodeDecodeError:
		op = no_punc(str(sentence))
	return op


def get_typology(sentence):
	"""
	takes a sentence as input
	returns an array indicating the subject, verb, object order
	"""
	def grammar_length():
		t = remove_punc(sentence) 
		tt = pos_tag(word_tokenize(t))
		index_list = [tt.index(item) for item in tt]
		tag_list = [tag[1] for tag in tt]
		return zip(index_list,tag_list)

	def check_order(grammar_array):
		g = grammar_array
		nn = ['NN','NNS','PRP','NNP'] # short list - expand as desired
		vb = ['VB','VBD','VBZ','VBG'] # short list - expand as desired
		try:
			verb_ = [item[0] for item in g if item[1] in vb][0]
			subject_ = [item[0] for item in g if item[1] in nn][0]
			object_  = [item[0] for item in g if item[1] in nn][-1]
			group = [[subject_,'subject'],[verb_,'verb'],[object_,'object']]	
		except IndexError:
			return 'Unknown'
		else:
			return sorted(group, key=lambda x: x[0])

	return check_order(grammar_length())

def define(word):
	start = time()

	def in_dictionary(word):
		l = []
		for i in en_dictionary:
			if i == word.encode('utf-8'): 
				l.append(i)
		if len(l) > 0:
			return True
		else:
			return False

	if in_dictionary(word) == False:
		return None
	else:
		language = 'en'
		word_id = word
		url = '%s%s/%s' % (address,language,word_id.lower())
		try:
			r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
		except ConnectionError as e:
			return None
		else:
			try:
				raw_dict = json.loads(json.dumps(r.json()))
			except simplejson.scanner.JSONDecodeError:
				return None
			definition = raw_dict['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
			end = time()
			return [word] + definition + [round(end-start,5)]

def read(text):
	# test sentence structure
	typology = [element[1] for element in get_typology(text)]
	sw = get_stopwords() # stop words
	tw = text.split() # total words
	words = set(text.split()) - sw	
	stopwords_found = [word for word in tw if word in sw]
	stopword_count = len(stopwords_found)
	word_count = len(text.split())

	def recognition():
		set_of_definitions = []
		st = LancasterStemmer()
		for word in words:
			try:
				dw = define(st.stem(word))
			except KeyError:
				dw = None
			if dw != None:
				set_of_definitions.append(dw)

		return set_of_definitions

	def output():
		op = {}
		definitions = recognition()
		definition_count = len(definitions)
		comp_time = [item[2] for item in definitions]
		total_comp_time = round(sum(comp_time),5)
		words_defined = [item[0] for item in definitions]
		word_definitions = [item[1] for item in definitions]
		op['sentence_typology'] = typology 
		op['total_words_read'] = word_count
		op['stopwords_found'] = stopwords_found
		op['comprehension_rate'] = round(float(definition_count+stopword_count) / float(word_count) * 100, 2)
		op['comprehension_time'] = total_comp_time
		op['reading_rate'] = '{} per word'.format(round(total_comp_time/word_count,4))
		op['defined_words'] = words_defined 
		op['definitions'] = word_definitions

		return op

	return output()

my_sentence = 'the quick brown fox jumped over the lazy dog'
print json.dumps(read(my_sentence))

