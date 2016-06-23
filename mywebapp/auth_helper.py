from urllib import urlencode
import requests
from config import client_id, client_secret
import json
import jwt
from datetime import datetime

# The OAuth authority.
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for consent.
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/authorize?{0}')

# The token issuing endpoint.
token_url = '{0}{1}'.format(authority, '/common/oauth2/token')


def validate_token(oauth_token):
    decoded = jwt.decode(oauth_token, verify=False)
    print "claims:", json.dumps(decoded, indent=4)
    exp = decoded['exp']
    valid = datetime.now() <= datetime.fromtimestamp(exp)
    if not valid:
        print "token expired"
    return valid


def get_signin_url(redirect_uri):
    # Build the query parameters for the signin URL.
    params = {'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code'
              }

    signin_url = authorize_url.format(urlencode(params))
    return signin_url


def get_token_on_behalf(user_token):
    # Build the post form for the token request
    post_data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
                 'assertion': user_token,
                 'client_id': client_id,
                 'client_secret': client_secret,
                 'resource': 'https://graph.microsoft.com',
                 'requested_token_use': 'on_behalf_of'
                 }

    r = requests.post(token_url, data=post_data)
    print "POST {0}".format(token_url)
    print json.dumps(post_data, indent=4)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


def get_token_refresh(refresh_token):
    # Build the post form for the token request
    post_data = {'grant_type': 'refresh_token',
                 'refresh_token': refresh_token,
                 'client_id': client_id,
                 'client_secret': client_secret,
                 'resource': 'https://graph.microsoft.com',
                 }

    r = requests.post(token_url, data=post_data)
    print "POST {0}".format(token_url)
    print json.dumps(post_data, indent=4)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

