from flask import Flask, request, jsonify, json
from flask_cors import CORS
import search

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def hello():
    return 'search functions'


@app.route('/api/search/<searchIndex>/<facet>/<filter>', methods=['POST'])
def getFacetedSearchResults(searchIndex, facet, filter):
    r = search.getSearchResults(request.get_data(as_text=True), searchIndex ,facet, filter)
    return jsonify(results = r)

@app.route('/api/search', methods=['POST'])
def getSearchResults():
    r = search.getSearchResults(request.get_data(as_text=True), facet = None, filter = None )
    return jsonify(results = r)

@app.route('/api/search/<searchIndex>', methods=['POST'])
def getSearchResultsInIndex(searchIndex):
    r = search.getSearchResults(request.get_data(as_text=True), searchIndex ,facet = None, filter = None )
    return jsonify(results = r)


@app.route('/api/indexes', methods=['GET'])
def getSearchIndex():
    r = search.getSearchIndex()
    return jsonify(results = r)