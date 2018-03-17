from flask import *
import requests
import sys
from threading import Timer
sys.path.append('../Reddit API')
import GetTop10
from Constants import *

app = Flask(__name__)

headers = None
token = None

@app.route('/')
def index():
    return render_template('index.html')


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
