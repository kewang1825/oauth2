from auth_helper import get_token_service_to_service
import json
import requests


def call_get_mail(access_token, user_id):
    rest_url = "http://localhost:5000/messages/{0}".format(user_id)
    header_data = {'Content-Type': 'application/json',
                   'Authorization': "Bearer {0}".format(access_token)
                   }

    print "GET {0}".format(rest_url)
    print json.dumps(header_data, indent=4)
    r = requests.get(rest_url, headers=header_data)

    try:
        return r.json()
    except:
        return 'Error getting messages: {0} - {1}'.format(r.status_code, r.text)


def main():
    token_response = get_token_service_to_service()
    print json.dumps(token_response, indent=4)
    access_token = token_response['access_token']

    result = call_get_mail(access_token, user_id="namprd21anchor@microsoft.onmicrosoft.com")
    print json.dumps(result, indent=4)


if __name__ == '__main__':
    main()
