from flask import *
import requests
import sys
import os
from threading import Timer

sys.path.append('..')
import main
from Constants import *

app = Flask(__name__, static_url_path='')

headers = None
token = None


@app.route('/')
def index():
    return send_from_directory('../Website/', 'index.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../Website/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../Website/css', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('../Website/img', path)


@app.route('/font-awesome/<path:path>')
def send_font_awesome(path):
    return send_from_directory('../Website/font-awesome', path)


@app.route('/color/<path:path>')
def send_color(path):
    return send_from_directory('../Website/color', path)

"""
@app.route('/get_top_posts_subreddits', methods=['POST'])
def get_top_posts():
    # try:
    n_posts = int(request.values.get('n_posts', '12'))
    time_period = request.values.get('time_period', 'day')
    return jsonify(GetTop10.get_top_posts_subreddits(n_posts, time_period))
    # except Exception as err:
    #     raise err
    #     return str(type(err)) + err.message

"""


@app.route('/get_top_subreddits', methods=['POST'])
def get_top_subreddits():
    n_posts = int(request.values.get('n_posts', '100'))
    time_period = request.values.get('time_period', 'day')
    return jsonify(main.getTopSubredits(n_posts, time_period))


@app.route('/get_top_categories', methods=['POST'])
def get_top_categories():
    n_posts = int(request.values.get('n_posts', '100'))
    time_period = request.values.get('time_period', 'day')
    return jsonify(main.getMostPopularCategories(n_posts, time_period))


@app.route('/get_top_results', methods=['POST'])
def get_top_results():
    n_posts = int(request.values.get('n_posts', '12'))
    n_comments = int(request.values.get('n_comments', '50'))
    time_period = request.values.get('time_period', 'day')
    return jsonify(main.getTopResults(n_posts, n_comments, time_period))



if __name__ == '__main__':
    main.initReddit()
    app.run(debug=True, port=65010)
