import json
import requests
import base64
from config import client_id, client_secret

# The OAuth authority.
authority = 'https://login.microsoftonline.com'

# The token issuing endpoint.
token_url = '{0}{1}'.format(authority, '/microsoft.com/oauth2/token')


# This function requests client credential flow to the token
# issuing endpoint, gets the service-to-service access token, and then returns it.
def get_token_service_to_service():
    # Build the post form for the token request
    post_data = {'grant_type': 'client_credentials',
                 'client_id': client_id,
                 'client_secret': client_secret,
                 'resource': 'http://localhost:5000/1/9646111a-31f7-11e6-a9a7-0f220aab2a15',
                 }

    print "POST {0}".format(token_url)
    print json.dumps(post_data, indent=4)
    r = requests.post(token_url, data=post_data)

    try:
        token_response = r.json()
        print "RESPONSE"
        print json.dumps(token_response, indent=4)
        return token_response["access_token"]
    except:
        print 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)
        return None


def exam_token(oauth_token, pos=1):
    # JWT is in three parts, header, token, and signature
    # separated by '.'
    token_parts = oauth_token.split('.')
    encoded_token = token_parts[pos]

    # base64 strings should have a length divisible by 4
    # If this one doesn't, add the '=' padding to fix it
    leftovers = len(encoded_token) % 4
    if leftovers == 2:
        encoded_token += '=='
    elif leftovers == 3:
        encoded_token += '='

    # URL-safe base64 decode the token parts
    decoded = base64.urlsafe_b64decode(encoded_token.encode('utf-8')).decode('utf-8')

    # Load decoded token into a JSON object
    return json.loads(decoded)
