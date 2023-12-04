from flask import Flask, render_template, request, redirect, url_for
from steam_scraper.run_spider import Scraper 

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
    # best quality
    # worst quality
    return f'Results for {game_name}'

if __name__ == '__main__':
    app.run(port=4999, debug=True)
