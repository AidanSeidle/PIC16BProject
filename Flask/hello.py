from flask import Flask, render_template, request, redirect, url_for
from steam_scraper.run_spider import Scraper 
from Analysis.TopicAnalysis import analyze_comments
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_name = request.form['game_name']
        return redirect(url_for('result', game_name=game_name))
    return render_template('index.html')

def get_comments(game_name):
    x = game_name.lower()
    x = x.split()
    x = '+'.join(x)

    scraper = Scraper()
    scraper.run_spiders(x)

@app.route('/result/<game_name>')
def result(game_name):
    get_comments(game_name)
    positive_topics, negative_topics = analyze_comments()
    return render_template('result.html', positive_topics=positive_topics, 
                            negative_topics=negative_topics)

if __name__ == '__main__':
    app.run(port=5000, debug=True)