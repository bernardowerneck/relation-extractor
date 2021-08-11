import nltk
import opennre

model = opennre.get_model('tacred_bert_softmax')

def analyze_sentences(sentences):
	return [prepare(model.infer(sentence)) for sentence in sentences]

def prepare(infered):
	return {
		"relation": infered[0],
		"prob": infered[1]
	}