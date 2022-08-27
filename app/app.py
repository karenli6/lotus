# app.py
from flask import Flask, jsonify, request, render_template
from utils import extract_key_terms, write_file
import os
import sys

sys.path.append('..')
from graph_generator import create_graph
from graph_to_d3 import graph_to_d3




app = Flask(__name__)

print("IN APP PY")

@app.route('/links', methods=['GET', 'POST'])
def links():
    print("IN LINKS")
    # POST request
    assert request.method == 'POST'
    print("incoming: ")
    # print(request.get_json())
    search_queries = [link for link in request.get_json()['urls'] if 'www.google.com/search' in link]
    # print(search_queries)
    final_array =extract_key_terms(search_queries)
    # print(final_array)
    ## dump final_array into csv file
    write_file(final_array)
    print('after write file')

    # create graph and collect sizes from search history data
    GRAPH, SIZES = create_graph()

    ## convert graph to d3 json object
    status = graph_to_d3(GRAPH, SIZES)
    assert status == True
    
    return 'OK', 200

if __name__ == "__main__":
  # Set environment variables
  # print("checking env variable", os.environ.get('PYTHONDONTWRITEBYTECODE'))
  os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
  app.run(debug=True)