# -*- coding: utf-8 -*-


from datetime import datetime
import requests
import random
import string
import pyotp
import sys
import json

#
# From src folder,
#  PYTHONPATH="." /usr/local/bin/python3.6 nwae/broadcaster/Example.py https://myaggregator.url/chat-aggregator/ username password
#
chat_aggregator_url = sys.argv[1]
# chat_aggregator_url = 'http://localhost:7002/cagg'
datetime_format = '%Y-%m-%d %H:%M:%S'

#
# 1. Create your subscriber ID & password
#
# cd /usr/local/bin/git/nwae/nwae.broadcaster/app.data/secret
# sudo vi staging.cf
#
username = sys.argv[2]
shared_secret = sys.argv[3]

s = shared_secret
# Pad to 8 modulo with last character in shared secret
shared_secret_pad = s + s[-1] * ((8 - len(s) % 8) % 8)
otp = pyotp.TOTP(shared_secret_pad).now()


#
# Push feed to Feed Aggregator
#
accId = 4
botId = 30
# chatId = ''.join(random.choices(string.ascii_lowercase, k=20))
chatId = '88asdfasdflllsldl'

msg = {
    "event": 0,
    "chatId": chatId,
    "campaignId": 123,
    "question": "你凭什么不努力 却还未很么都想要",
    "intentId": None,
    "location": None,
    "formValues": None
}
data = {
    'provider': username,
    'auth': otp,
    'accId': accId,
    'botId': botId,
    'chatId': chatId,
    'datetime': str(datetime.now().strftime(datetime_format)),
    'msg': msg,
    'speaker': 'Client',
    'speakerName': 'Client'
}
restResponse = requests.post(
    url     = chat_aggregator_url,
    json    = data,
    # No need to verify HTTPS
    verify  = False,
    timeout = 1.0
)
print('Sending data: ' + str(data))
if restResponse.ok:
    print('Server Reply: ' + str(restResponse.text))
else:
    print('Send FAIL')

#
# Pull Feed
#
data = {
    'mode': 'pull',
    'chatId': chatId,
    'user': username,
    'auth': otp
}

restResponse = requests.post(
    url     = chat_aggregator_url,
    json    = data,
    # No need to verify HTTPS
    verify  = False,
    timeout = 1.0
)
if restResponse.ok:
    print('Server response OK.')
    print(restResponse.text)
    data = json.loads(restResponse.content)
    print(type(data))
    for i in range(len(data)):
        print(str(i) + '. ' + str(data[i]))
