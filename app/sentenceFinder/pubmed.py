#!/usr/bin/python
import requests
import xmltodict
import re
import nltk
import functools


# Fetch the article ids 
base_article_search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term="

# Fetch article data from id
base_specific_article_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="

# armazena a resposta da requisição em response
response = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?term=iron,copper')

# transforma o xml da resposta em um dicionario
responseAsDict = xmltodict.parse(response.text)

# Pega a lista de ids recebidos
idList = responseAsDict['eSearchResult']['IdList']['Id']

# Url base de requisição de artigo no pubMed
baseString = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id="

# adicionando o id do artigo que quero na url
newUrl = baseString + idList[0]

# Requisição para buscar o artigo desejado
r2 = requests.get(newUrl).text

abstract_matcher = re.compile("abstract \"((?:.*\n)*?.*)\",")

# abstract = prog.findall(r2)[0].replace("\n", "")

def fetchSamples(word1, word2):
	article_search_url = base_article_search_url + word1 + "," + word2
	article_id_list = xmltodict.parse(requests.get(article_search_url).text)['eSearchResult']['IdList']['Id']
	return [fetchArticleAbstract(article_id) for article_id in article_id_list]

def fetchArticleAbstract(article_id):
	article_url = base_specific_article_url + article_id
	abstract = abstract_matcher.findall(requests.get(article_url).text)
	return abstract[0].replace("\n", "") if len(abstract) > 0 else ""

def sentence_marker(word1, word2):
	def mark_sentence(sentence):
		marked = {'text': sentence}
		pos_h = sentence.lower().find(word1.lower())
		marked['h'] = {'pos': (pos_h, pos_h + len(word1))}
		pos_t = sentence.lower().find(word2.lower())
		marked['t'] = {'pos': (pos_t, pos_t + len(word2))}
		return marked
	return mark_sentence

def find_sentences(abstract, word1, word2):
	has_word1 = word_finder(word1)
	has_word2 = word_finder(word2)


	sentences = nltk.sent_tokenize(abstract)

	def has_both(sentence):
		return has_word1(sentence) and has_word2(sentence)

	mark_sentence = sentence_marker(word1, word2)

	return [mark_sentence(sentence) for sentence in sentences if has_both(sentence)]

def word_finder(target_word):
	def find_word_in_sentence(sentence):
		return sentence.upper().find(target_word.upper()) != -1
	return find_word_in_sentence

def find_in_doc(doc, word1, word2):
	raw = open(doc, "r").read()
	sentences = nltk.sent_tokenize(raw)
	return find_sentences(sentences, word1, word2)

def prepare_sentences(h, t):
	abstracts = fetchSamples(h,t)
	sent_list = [find_sentences(abstract,h,t) for abstract in abstracts]
	return functools.reduce(lambda a, b: a + b, sent_list)
