from app import app
from flask import request, jsonify
import app.sentenceFinder as finder
import app.sentenceAnalyzer.analyzer as analyzer

@app.route('/')
@app.route('/index')
def index():
	return 'Hello World'

@app.route('/singlerelationfinder', methods = ['POST'])
def single_relation_finder():
	json = request.get_json(force=True)
	head = json.get('head')
	tail = json.get('tail')
	module = json.get('module')
	return jsonify(analyzer.analyze_sentences(finder.prepare_sentences(head,tail, module))) 

@app.route('/listrelationfinder', methods = ['POST'])
def list_relation_finder():
	json = request.get_json(force=True)
	pairs = json.get('pairs')
	module = json.get('module')
	results = [prepare(pair, module) for pair in pairs]
	analize(results)
	return jsonify(results) 


def prepare(element, module):
	try:
		results = analyzer.analyze_sentences(finder.prepare_sentences(element.get("head"),element.get("tail"), module))
	except:
		results = "failed"

	return {
		"head": element.get("head"),
		"tail": element.get("tail"),
		"results": results
	}

def analize(results):
	sentence_count = 0
	relation_result = {}
	total_searched = len(results)
	failed_count = 0
	for result in results:
		if result["results"] == "failed":
			failed_count += 1
			continue
		for subresult in result["results"]:
			sentence_count += 1
			if subresult["relation"] in relation_result:
				relation_result[subresult["relation"]] += 1
			else:
				relation_result[subresult["relation"]] = 1

	print("sentence_count: ")
	print(sentence_count)
	print("relation_result: ")
	print(relation_result)
	print("total_searched: ")
	print(total_searched)
	print("failed_count: ")
	print(failed_count)