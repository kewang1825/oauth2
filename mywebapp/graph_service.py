import requests
import uuid
import json

# The base URL for the Microsoft Graph API.
graph_api_endpoint = 'https://graph.microsoft.com/v1.0{0}'


def call_me_endpoint(access_token):
    # The resource URL for the sendMail action.
    me_url = graph_api_endpoint.format('/me/')

    # Set request headers.
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true'
    }
    headers.update(instrumentation)

    print "GET {0}".format(me_url)
    print json.dumps(headers, indent=4)
    r = requests.get(url=me_url, headers=headers)

    try:
        return r.json()
    except:
        return 'Error retrieving user info: {0} - {1}'.format(r.status_code, r.text)


def call_send_mail_endpoint(access_token, email_text, email_address):
    # The resource URL for the sendMail action.
    send_mail_url = graph_api_endpoint.format('/me/sendMail')

    # Set request headers.
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true'
    }
    headers.update(instrumentation)

    # Create the email that is to be sent with API.
    email = {
        'Message': {
            'Subject': 'Connect MileIQ to Office 365',
            'Body': {
                'ContentType': 'HTML',
                'Content': email_text,
            },
            'ToRecipients': [
                {
                    'EmailAddress': {
                        'Address': email_address
                    }
                }
            ]
        },
        'SaveToSentItems': 'true'
    }

    print "POST {0}".format(send_mail_url)
    print json.dumps(headers, indent=4)
    response = requests.post(url=send_mail_url, headers=headers, data=json.dumps(email), params=None)
    return {"status": response.status_code, "details": response.text}


def call_messages_endpoint(access_token):
    # The resource URL for the sendMail action.
    message_url = graph_api_endpoint.format('/me/messages?$select=Subject,ReceivedDateTime')

    # Set request headers.
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = {
        'client-request-id': request_id,
        'return-client-request-id': 'true'
    }
    headers.update(instrumentation)

    print "GET {0}".format(message_url)
    print json.dumps(headers, indent=4)
    response = requests.get(url=message_url, headers=headers)
    return {"status": response.status_code, "details": response.text}
