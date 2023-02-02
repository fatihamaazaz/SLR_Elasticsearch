from flask import Flask , render_template , url_for , request, redirect, Markup

import json
import codecs
import pyodbc 
from tqdm.notebook import tqdm
from elasticsearch import Elasticsearch
import requests
set

es = Elasticsearch(['http://localhost:9200'])
#es = Elasticsearch(['http://localhost:9200'], http_auth=('', ''))




app = Flask(__name__ , template_folder = 'templates')

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/" , methods=["GET","POST"])
def search():
    if request.method == "POST" :
        search_input = request.form["search-query"]
        query_body = {
            "track_total_hits": True,
            "size":10000,
            "query": {
            "bool": {
            "must": [
                { "match": { "Document Type": "Article"}},
                { "fuzzy": {"Abstract": "diabetic"}},
                { "fuzzy": {"Abstract": "retinopathy"}},
                { "fuzzy": {"Abstract": "detection"}},
                { "fuzzy": {"Abstract": "technique~"}}
            ],
            "should": [
                { "match": { "Document Type": "Article" } },
                { "match": { "Document Type": "Journal" } },
                { "match": { "Document Type": "Research Paper" } },
                { "match": { "Abstract": search_input } },
                { "match": { "Title": search_input } },
                { "fuzzy": {"Abstract":"solution"}},
                { "fuzzy": {"Abstract": "link"}},
                { "fuzzy": {"Abstract":"data"}},
            ],
                "must_not": [
                { "match": { "Link": "Not Found"}}
            ],
            "filter": [
                { "range": { "Year": { "gte": "2012" } } }
            ],
                "minimum_should_match": 1,
            }
        }
        }
        result = es.search(index="index_slr_documents", body=query_body)
        return render_template('table.html',result=result)


@app.route('/data/<dt>', methods=['GET','POST'])

def data(dt):
    #d = str_to_dict(str(dt))
    result = es.get(index="index_slr_documents", id=dt)
    return render_template('data.html', data=result)


if __name__ == "__main__":
    app.run()