from flask import Flask, url_for, request, redirect, render_template
from auth_helper import get_signin_url, get_user_token
import json
import jwt

app = Flask(__name__)


@app.route('/index/<string:token>')
def index(token):
    return render_template('index.html', token=token)


@app.route('/')
def login():
    redirect_url = url_for('hello', _external=True)
    login_url = get_signin_url(redirect_url)
    return redirect(login_url)


@app.route('/hello', methods=['GET'])
def hello():
    redirect_url = url_for('hello', _external=True)

    error = request.args.get('error', '')
    if error != '':
        return 'Error:\n' + error + " " + request.args.get('error_description', '')

    code = request.args.get('code', '')
    token_response = get_user_token(redirect_url, code)
    print json.dumps(token_response, indent=4)

    if 'error' in token_response:
        return 'Error:\n' + token_response['error_description']

    access_token = token_response['access_token']

    try:
        decode = jwt.decode(access_token, verify=False)
        print "ACCESS_TOKEN"
        print json.dumps(decode, indent=4)
    except:
        print 'Failed to decode the access token'

    return redirect(url_for('index', token=access_token))


if __name__ == '__main__':
    app.run(debug=True, host="localhost")
