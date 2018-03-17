from flask import *
import requests
import sys
from threading import Timer

sys.path.append('../Reddit API')
import GetTop10
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


@app.route('/get_top_posts_subreddits', methods=['POST'])
def get_top_posts():
    # try:
    n_posts = int(request.values.get('n_posts', '12'))
    time_period = request.values.get('time_period', 'day')
    return jsonify(GetTop10.get_top_posts_subreddits(n_posts, time_period))
    # except Exception as err:
    #     raise err
    #     return str(type(err)) + err.message


if __name__ == '__main__':
    GetTop10.refresh_token()
    app.run(debug=True, port=65010)
