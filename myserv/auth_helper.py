import json
import requests
from config import client_id, client_secret

# The OAuth authority.
authority = 'https://login.microsoftonline.com'

# The token issuing endpoint.
token_url = '{0}{1}'.format(authority, '/72f988bf-86f1-41af-91ab-2d7cd011db47/oauth2/token')


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
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)
