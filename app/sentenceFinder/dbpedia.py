import requests
import json

def query(q, f='application/json'):
    try:
        params = {'query': q}
        resp = requests.get(dbpedia, params=params, headers={'Accept': f})
        return json.loads(resp.text)
    except Exception as e:
        print(e, file=sys.stdout)
        raise

query_base =  """ 
    PREFIX purl: <http://purl.org/dc/terms/>
    PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>

    select distinct ?abstract ?label where {
        <http://dbpedia.org/resource/REPLACE> rdfs:label ?label .
        <http://dbpedia.org/resource/REPLACE> dbo:abstract ?abstract
        FILTER (lang(?label) = 'en')
        FILTER (lang(?abstract) = 'en')
    } LIMIT 100
    """

dbpedia = "https://dbpedia.org/sparql"

def find_abstract(word):
    query_string = query_base.replace("REPLACE", word.capitalize())
    return query(query_string)["results"]["bindings"][0]["abstract"]["value"]

def prepare_sentences(word1, word2):
    abst1 = find_abstract(word1)
    abst2 = find_abstract(word2)
    result = []
    if find_word_in_sentence(abst1, word1, word2):
        result.append(mark_sentence(abst1, word1, word2))
    if find_word_in_sentence(abst2, word1, word2):
        result.append(mark_sentence(abst2, word1, word2))
    return result

def mark_sentence(sentence, word1, word2):
    marked = {'text': sentence}
    pos_h = sentence.lower().find(word1.lower())
    marked['h'] = {'pos': (pos_h, pos_h + len(word1))}
    pos_t = sentence.lower().find(word2.lower())
    marked['t'] = {'pos': (pos_t, pos_t + len(word2))}
    return marked

def find_word_in_sentence(sentence, word1, word2):
    return sentence.upper().find(word1.upper()) != -1 and sentence.upper().find(word2.upper()) != -1