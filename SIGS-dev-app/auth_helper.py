from urllib import urlencode
import requests
from config import client_id, client_secret
import json

# The OAuth authority.
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for consent.
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/authorize?{0}')

# The token issuing endpoint.
token_url = '{0}{1}'.format(authority, '/common/oauth2/token')


def get_signin_url(redirect_uri):
    # Build the query parameters for the signin URL.
    params = {'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code',
              'prompt': 'consent'
              }

    signin_url = authorize_url.format(urlencode(params))
    return signin_url


def get_user_token(redirect_uri, code):
    # Build the post form for the token request
    post_data = {'grant_type': 'authorization_code',
                 'code': code,
                 'client_id': client_id,
                 'client_secret': client_secret,
                 'resource': 'https://outlook.office.com',
                 'redirect_uri': redirect_uri,
                 }

    r = requests.post(token_url, data=post_data)
    print "POST {0}".format(token_url)
    print json.dumps(post_data, indent=4)

    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)


