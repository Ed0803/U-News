from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    
    # Call the scraper function
    results = scrape_news(query)
    return jsonify(results)

def scrape_news(query):
    url = f"https://www.google.com/search?q={query}+news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    articles = []
    for item in soup.select('.tF2Cxc'):  # Google search result container
        title = item.select_one('.DKV0Md').text
        link = item.select_one('.yuRUbf a')['href']
        snippet = item.select_one('.IsZvec').text
        articles.append({'title': title, 'link': link, 'snippet': snippet})
    
    return articles

if __name__ == '__main__':
    app.run(debug=True)
