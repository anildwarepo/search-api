import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import os

def sortSearchScore(e):
  return e['@search.score']


def getSearchIndex():
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'api-key': os.getenv('SEARCH_API_KEY'),
    }
    try:
        conn = http.client.HTTPSConnection(os.getenv('SEARCH_ENDPOINT'))
        conn.request("GET", "/indexes?api-version=2020-06-30-Preview&$select=name", None ,headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data.decode('utf8'))
        conn.close()
        return jsondata
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getSearchResults(searchTerm, searchIndex ,facet, filter):
    
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'api-key': os.getenv('SEARCH_API_KEY'),
    }

    
    params = urllib.parse.urlencode({
        
    })    

    if filter is not None or facet is not None:
        filter = f"{facet}/any(p: p eq '{filter}')"
        facet = [f"facet={facet}"]
    else:
        filter = ""
        facet = []

    searchBody = {
        "search": searchTerm,
        "queryType": "semantic",
        "speller": "lexicon",
        "queryLanguage":"en-us",
        "facets":[],
        "filter": filter,
        "highlight": "content",
        "searchFields":"content, keyphrases,people,organizations,locations",
        "answers": "extractive|count-3",
        "select":"content,keyphrases,people,organizations,locations,metadata_storage_path",
        "top": 10,
        "count": True
    }
    people = []
    organizations = []
    locations = []
    keyphrases = []
    #searchResults = {"results":}
    try:
        conn = http.client.HTTPSConnection(os.getenv('SEARCH_ENDPOINT'))
        conn.request("POST", f"/indexes/{searchIndex}/docs/search?api-version=2020-06-30-Preview%s" % params, json.dumps(searchBody), headers)
        response = conn.getresponse()
        data = response.read()
        jsondata = json.loads(data.decode('utf8'))
        #jsondata['value'].sort(reverse=True, key=sortSearchScore)
        searchResults = {"searchResults": jsondata, "people": people, "locations": locations, "organizations": organizations, "keyphrases": keyphrases }
        for v in jsondata['value']:
            for p in v['people']:
                if not p in people:
                    people.append(p)
            for l in v['locations']:
                if not l in locations:
                    locations.append(l)
            for o in v['organizations']:
                if not o in organizations:
                    organizations.append(o)
            for k in v['keyphrases']:
                if not k in keyphrases:
                    keyphrases.append(k)

        conn.close()
        return searchResults
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))