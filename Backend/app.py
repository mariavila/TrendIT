from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_top_posts'):
    n_posts=

if __name__ == '__main__':
    app.run(debug=True, port=65010)
