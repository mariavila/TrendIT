import requests
import requests.auth
from flask import *
from Constants import *

app = Flask(__name__)


@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()


@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        # Uh-oh, this request wasn't started by us!
        abort(403)
    code = request.args.get('code')
    # We'll change this next line in just a moment
    token_json = get_token(code)
    refresh_token = token_json["refresh_token"]

    return "Your refresh token is %s" % refresh_token


def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "permanent",
              "scope": "identity read"}
    import urllib
    url = API + "authorize?" + urllib.urlencode(params)
    return url


def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = {"User-agent": USER_AGENT}
    response = requests.post(API + "access_token",
                             auth=client_auth,
                             data=post_data,
                             headers=headers)
    token_json = response.json()

    return token_json


def get_username(access_token):
    headers = {"Authorization": "bearer " + access_token,
               "User-agent": USER_AGENT}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
    pass


def is_valid_state(state):
    return True


if __name__ == '__main__':
    app.run(debug=True, port=65010)
