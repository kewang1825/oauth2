from auth_helper import get_token_service_to_service, exam_token
from config import messages_url
import json
import requests


def call_get_mail(access_token, user_id):
    rest_url = "{0}/{1}".format(messages_url, user_id)
    header_data = {'Content-Type': 'application/json',
                   'Authorization': "Bearer {0}".format(access_token)
                   }

    print "GET {0}".format(rest_url)
    print json.dumps(header_data, indent=4)
    r = requests.get(rest_url, headers=header_data)

    try:
        return r.json()
    except:
        return {"status": r.status_code, "details": r.text}


def main():
    access_token = get_token_service_to_service()
    if access_token is not None:
        decode = exam_token(access_token)
        print "ACCESS_TOKEN"
        print json.dumps(decode, indent=4)
        result = call_get_mail(access_token, user_id="namprd21anchor@microsoft.onmicrosoft.com")
        print "RESPONSE"
        print json.dumps(result, indent=4)


if __name__ == '__main__':
    main()
