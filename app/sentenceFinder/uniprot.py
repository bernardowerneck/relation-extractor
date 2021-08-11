import requests
import json

def query(q, f='application/json'):
    try:
        params = {'query': q}
        resp = requests.get(uniprot, params=params, headers={'Accept': f})
        return json.loads(resp.text)
    except Exception as e:
        print(e, file=sys.stdout)
        raise

query_base =  """ 
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX up: <http://purl.uniprot.org/core/>

    select distinct ?sub ?subLabel ?obj ?objType ?objLabel ?label where {
      ?sub rdfs:seeAlso ?obj .
      OPTIONAL {?sub skos:prefLabel ?subLabel .}
      ?sub a up:Disease .
      ?obj a ?objType .
      OPTIONAL {?obj skos:prefLabel ?objLabel .}
      ?objType rdfs:label ?label
    } LIMIT 100

    """

uniprot = "https://sparql.uniprot.org/sparql"

def related():
    return query(query_base)["results"]["bindings"]