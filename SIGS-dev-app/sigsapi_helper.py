import requests
from config import client_id
import json
from datetime import datetime

signals_url = 'https://outlook.office.com/api/v2.0/me/signals'

def sigs_get_signals(token):
    # Build the query parameters for the signals URL.
    params = {'$orderby': 'StartTime desc',
              '$top': 1,
              }

    headers = {'Prefer': 'exchange.behavior="SignalAccessV2,OpenComplexTypeExtensions"',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token,
              }

    r = requests.get(signals_url, params=params, headers=headers)
    print "GET {0}".format(r.url)
    print r.text

    try:
        return r.json()
    except:
        return 'Error getting signals: {0} - {1}'.format(r.status_code, r.text)


def sigs_post_signal(token, signal, customproperties=None):
    # Build the post form for the signal request
    post_data = {'SignalType': signal,
                 'StartTime': datetime.now().isoformat() + '-07:00',
                 'EndTime': datetime.now().isoformat() + '-07:00',
                 'Compliance': 'SystemMetaData',
                 'Status': 'Completed',
                 'Locale': 'en-US',
                 'Application': {
                     'AadAppId': client_id,
                     'AppName': 'SIGS-dev-app',
                     'Workload': 'EXO',
                    },
                 'Actor': {
                     'ActorType': 'User',
                     'ActorIdType': 'AAD',
                     'ActorId': 'Self',
                    },
                 }

    headers = {'Prefer': 'exchange.behavior="SignalAccessV2,OpenComplexTypeExtensions,EhamJitProvisioning",outlook.data-source="Substrate"',
               'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + token,
              }

    r = requests.post(signals_url, json=post_data, headers=headers)
    print "POST {0}".format(signals_url)
    print json.dumps(post_data, indent=4)
    print r.status_code
    return r.text



