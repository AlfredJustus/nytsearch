from flask import Flask, render_template, request
import requests
from datetime import datetime


app = Flask(__name__)

BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
KEY = "nx4m4JOlA0ESJtJKfxJ7YChL5G5ELwXx"

#searches the API for the given search term
def search(search_term):
    params = {
        "q": search_term,
        "api-key": KEY
    }
    response = requests.get(BASE_URL, params)
    return response.json()



@app.route("/", methods=["GET", "POST"])
#gets search term, searches for the results, formats the results
def index():
    if request.method == "POST":
        search_term = request.form["search_term"]
        search_results = search(search_term)
        results = format_results(search_results)
        return render_template("results.html", results=results, search_term=search_term)
    return render_template("index.html", results=[])

# formats the received results 
def format_results(search_results):
    docs = search_results['response']['docs']
    formatted_results = []
    for doc in docs:
        date_string = doc['pub_date']
        date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z").date()
        formatted_date = date_obj.strftime("%d.%m.%Y")
        url = doc['web_url']
        article_headline = doc['headline']['main']

        formatted_results.append ({
            'date': formatted_date,
            'headline': article_headline,
            'url': url,
        })
    return formatted_results




if __name__ == "__main__":
    app.run(debug=True)
