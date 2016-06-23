from flask.ext.httpauth import HTTPTokenAuth
from flask import Flask, jsonify, abort, make_response, request, redirect
from auth_helper import get_token_on_behalf, get_token_refresh, get_signin_url, validate_token
from graph_service import call_me_endpoint, call_send_mail_endpoint, call_messages_endpoint
from token_cache import TokenCache
import json

app = Flask(__name__)
tokens = TokenCache()
auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    if 'Authorization' not in request.headers:
        # Unauthorized
        print 'No Authorization in header'
        return False
    else:
        authz = request.headers.get('Authorization');
        parts = authz.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            print 'OAuth is required'
            return False
        return validate_token(parts[1])


@app.route('/')
def login():
    login_url = get_signin_url('http://localhost:5000/hello')
    return redirect(login_url)


@app.route('/hello')
def hello():
    return 'Hello!'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/sendmail/<string:email_address>', methods=['POST'])
@auth.login_required
def send_mail(email_address):
    if not tokens.contains(email_address):
        user_token = request.headers.get('Authorization')[7:]
        token_response = get_token_on_behalf(user_token)
        print json.dumps(token_response, indent=4)

        access_token = token_response['access_token']
        refresh_token = token_response['refresh_token']
        user_info = call_me_endpoint(access_token)
        print json.dumps(user_info, indent=4)
        tokens.set(user_info['userPrincipalName'], refresh_token)
    else:
        cached_token = tokens.get(email_address)
        print 'using cache:'
        print json.dumps(cached_token, indent=4)

        token_response = get_token_refresh(cached_token['refresh_token'])
        print json.dumps(token_response, indent=4)
        access_token = token_response['access_token']

        user_info = call_me_endpoint(access_token)
        print json.dumps(user_info, indent=4)

    result = call_send_mail_endpoint(access_token, str(user_info), email_address)
    print json.dumps(result, indent=4)

    return make_response(result['details'], result['status'])


@app.route('/messages/<string:user_id>', methods=['GET'])
@auth.login_required
def get_mail(user_id):
    if not tokens.contains(user_id):
        # Unauthorized
        return make_response('No token available', 401)

    cached_token = tokens.get(user_id)
    print 'using cache:'
    print json.dumps(cached_token, indent=4)

    token_response = get_token_refresh(cached_token['refresh_token'])
    print json.dumps(token_response, indent=4)
    access_token = token_response['access_token']

    result = call_messages_endpoint(access_token)
    print json.dumps(result, indent=4)

    return make_response(result['details'], result['status'])


if __name__ == '__main__':
    app.run(debug=True)
