from flask import Flask,request, jsonify,render_template

import hashlib

app = Flask(__name__, template_folder='Template')
url_database = {}

@app.route('/')
def index():
    return render_template('shortner.html')

def generate_short_url(long_url):
    sha1_hash = hashlib.sha1(long_url.encode()).hexdigest()[:6]
    return f"https://short.url/{sha1_hash}"

@app.route('/shorten', methods = ['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_url = generate_short_url(long_url)
    url_database[short_url] = {'long_url':long_url,'hits': 0}
    return jsonify({'short_url': short_url})

@app.route('/search', methods=['GET'])
def search_url():
    term = request.args.get('term')
    results = []
    for short_url, data in url_database.items():
        if term.lower() in data['long_url'].lower():
            results.append({'title': data['long_url'], 'url': short_url})
    return jsonify(results)

@app.route('/<short_url>',methods = ['GET'])
def redirect_to_long_url(short_url):
    if short_url in url_database:
        url_database[short_url]['hits'] +=1
        return jsonify({'long_url': url_database[short_url]['long_url'], 'hits': url_database[short_url]['hits']})
    else:
        return jsonify({'error': 'Short URL not found'}),404
    
if __name__ == '__main__':
    app.run(debug=True)