#!/usr/bin/python
from app.sentenceFinder import pubmed
from app.sentenceFinder import dbpedia
from app.sentenceFinder import finder

modules = {
	"pubmed": pubmed.prepare_sentences,
	"dbpedia": dbpedia.prepare_sentences,
	"finder": finder.prepare_sentences
}

def prepare_sentences(head, tail, module):
	return modules[module](head, tail)