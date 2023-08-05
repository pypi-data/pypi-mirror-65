# -*- coding: utf-8 -*-

import websockets
import asyncio
import json
import re
import ssl
import certifi
import sys
import hashlib
from datetime import datetime
import pyotp


class SampleBroadcasterClient:

    # 'challenge', 'totp-style', or 'totp'
    AUTH_METHOD = 'totp'

    @staticmethod
    async def start_ws_client(
            server_uri,
            username,
            secret
    ):
        ws_client = SampleBroadcasterClient(
            server_uri = server_uri,
            username   = username,
            secret     = secret
        )
        await ws_client.run()

    def __init__(
            self,
            server_uri,
            username,
            secret
    ):
        if sys.version_info < (3, 7, 0):
            raise Exception(
                'Python version ' + str(sys.version) + ' not supported'
            )

        self.server_uri = server_uri
        self.username = username
        self.secret = secret

        return

    async def init_ws(
            self
    ):
        #
        # We need to do this to make sure it won't fail SSL Cert verification
        #
        ssl_context = None
        need_ssl = re.match(pattern='^(wss:)', string=self.server_uri)
        if need_ssl:
            ssl_context = ssl.create_default_context()
            ssl_context.load_verify_locations(certifi.where())

        self.ws = await websockets.connect(
            self.server_uri,
            ssl = ssl_context
        )
        print('Websocket to "' + str(self.server_uri) + '" formed..')

        # Receive challenge packet
        pkt = await self.ws.recv()
        pkt_json = json.loads(pkt)

        print('Authenticating using method "' + str(SampleBroadcasterClient.AUTH_METHOD) + '"...')

        if SampleBroadcasterClient.AUTH_METHOD == 'totp-style':
            now = datetime.now()
            str_now = now.strftime('%Y-%m-%d %H:%M:%S')
            str_challenge = str_now + self.secret
        elif SampleBroadcasterClient.AUTH_METHOD == 'totp':
            s = str(self.secret)
            # Pad to 8 modulo with last character in shared secret
            shared_secret_pad = s + s[-1] * ((8 - len(s) % 8) % 8)
            obj = pyotp.TOTP(shared_secret_pad)
            str_challenge = obj.now()
            print('TOTP OTP = ' + str(str_challenge))
        else:
            str_challenge = pkt_json['challenge']
            print('Received challenge string "' + str(pkt_json))
            str_challenge = str_challenge + self.secret

        str_test_challenge = str_challenge

        if SampleBroadcasterClient.AUTH_METHOD != 'totp':
            str_challenge_encode = str_challenge.encode(encoding='utf-8')
            print('Taking hash of ' + str(str_challenge_encode))
            h = hashlib.sha256(str_challenge_encode)
            str_test_challenge = h.hexdigest()

        # Strong Authentication: Send test challenge
        send_pkt = {
            'id': self.username,
            'testChallenge': str_test_challenge,
            'method': SampleBroadcasterClient.AUTH_METHOD
        }
        await self.ws.send(json.dumps(send_pkt, ensure_ascii=False).encode('utf-8'))
        print('Sent test challenge string:\n\r' + str(send_pkt))

        server_reply = await self.ws.recv()
        # print(server_reply)
        print('Server reply (type ' + str(type(server_reply)) + '): ' + str(server_reply))
        return

    async def handle_ws(
            self
    ):
        while True:
            packet = await self.ws.recv()
            try:
                json_pkt = json.loads(packet)
                provider = None
                timestamp = None
                acc_id = None
                bot_id = None
                if 'datetime' in json_pkt.keys():
                    timestamp = json_pkt['datetime']
                if 'accId' in json_pkt.keys():
                    acc_id = json_pkt['accId']
                if 'botId' in json_pkt.keys():
                    bot_id = json_pkt['botId']

                print('Bot ' + str(acc_id) + ':' + str(bot_id) + ' ' + str(timestamp) + ': ' + str(packet))
            except Exception as ex:
                print('Could not get server response. Exception "' + str(ex) + '"')

    async def run(self):
        await self.init_ws()
        #
        # Even if we run both together, they are not multi-threading, just asynchronous.
        # Thus ping function will still need to wait for the blocking input() call.
        #
        await asyncio.gather(
            self.handle_ws()
        )


if __name__ == '__main__':
    print('Args: ' + str(sys.argv))
    try:
        uri = sys.argv[1]
        username = sys.argv[2]
        secret = sys.argv[3]
    except:
        uri = 'ws://localhost:7003/livestream'
        username = 'anyone'
        secret = 'parasite'
        print('Exception getting URI from command line. Using default "' + str(uri) + '".')

    print('Connecting to "' + str(uri) + '", using username "' + str(username) + '", secret "' + str(secret) + '".')
    asyncio.run(SampleBroadcasterClient.start_ws_client(
        # We expect the URI (e.g. wss://mydomain.com/feed/
        server_uri = uri,
        username   = username,
        secret     = secret
    ))
    exit(0)

# asyncio.get_event_loop().run_until_complete(
#     WsClient.chat(server = 'local')
# )
