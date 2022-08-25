# app.py
from flask import Flask, jsonify, request, render_template
from utils import extract_key_terms, write_file
app = Flask(__name__)

@app.route('/todays_urls', methods=['POST'])
def hello():
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
    return 'OK', 200

if __name__ == "__main__":
  app.run(debug=True)