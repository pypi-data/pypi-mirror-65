#
# send a message to a discord channel using webhooks
#
# author:   Jean-Luc.Szpyrka@inria.fr
# creation: 10th day after the First Great French Quarantine
#

import sys    as sys

# https://realpython.com/python-requests/
import requests as requests

def notify(message, webhook):
    response = requests.post(
        'https://discordapp.com/api/webhooks/'+webhook,
        json={"content": message}
    )
    code = response.status_code
    if ( code < 200 or code >= 300):
        print("Something went wrong, verify the webhook")
        sys.exit(-1)
