from flask import Flask, render_template, request, redirect, url_for
from steam_scraper.run_spider import Scraper 
from Analysis.TopicAnalysis import analyze_comments
app = Flask(__name__)

def get_comments(game_name):
    """
    Processes game_name and sets the Scrapy spider crawling. 
    
    Args:
        game_name (str): user inputed name of a video game on Steam 
    """
    x = game_name.lower()
    x = x.split()
    x = '+'.join(x)

    scraper = Scraper()
    scraper.run_spiders(x)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        game_name = request.form['game_name']
        return redirect(url_for('result', game_name=game_name))
    return render_template('index.html')

@app.route('/result/<game_name>')
def result(game_name):
    get_comments(game_name)
    positive_topics, negative_topics = analyze_comments()
    return render_template('result.html', game_name=game_name, positive_topics=positive_topics, 
                            negative_topics=negative_topics)

if __name__ == '__main__':
    app.run(port=5000, debug=True)