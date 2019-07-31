from flask import Flask, url_for, request, redirect, render_template, jsonify, session
from flask_cors import CORS, cross_origin
from auth_helper import get_signin_url, get_user_token
from sigsapi_helper import sigs_get_signals, sigs_post_signal
import json
import jwt

app = Flask(__name__)
#app.secret_key = "super secret key"

@app.route('/index', methods=['GET'])
def index():
    token = request.args.get('token')
    if not token:
        token = session.get('token')

    return render_template('index.html', token=token)


@app.route('/', methods=['GET'])
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

    session['token'] = access_token
    return redirect(url_for('index'))


@app.route('/api/getsignals', methods=['GET'])
@cross_origin()
def get_signals():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        token = session.get('token')

    signals_response = sigs_get_signals(token)
    if 'error' in signals_response:
        return jsonify(error = signals_response['error'])

    signals = signals_response['value']

    print "VALUE"
    print json.dumps(signals, indent=4)
    return jsonify(value = signals)


@app.route('/api/postsignal', methods=['POST', 'GET'])
@cross_origin()
def post_signal():
    signal = request.args.get('signal')

    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(" ")[1]
    else:
        token = session.get('token')

    return sigs_post_signal(token, signal)


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
    #app.run(debug=True, host='localhost', ssl_context='adhoc')
