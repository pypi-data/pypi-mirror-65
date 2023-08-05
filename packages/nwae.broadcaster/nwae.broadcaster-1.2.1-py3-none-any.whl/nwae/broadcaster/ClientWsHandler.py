# -*- coding: utf-8 -*-

from geventwebsocket.websocket import WebSocket
from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
import sys
from nwae.broadcaster.SubscriberList import SubscriberList
import json
from nwae.broadcaster.Authenticate import Authenticate
from nwae.broadcaster.subscriber.SubscriberSharedSecret import SubscriberSharedSecret


class ClientWsHandler:

    STR_ENCODING = 'utf-8'

    #
    # Created for each connection
    #
    @staticmethod
    def ConnectionHandler(
            environ,
            start_response
    ):
        path = environ["PATH_INFO"]
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Environ: ' + str(environ)
        )

        if path == "/livestream":
            try:
                remote_addr = environ['HTTP_X_REAL_IP']
            except Exception:
                Log.error(
                    str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': No key "HTTP_X_REAL_IP" in environ.'
                )
                try:
                    remote_addr = environ['HTTP_X_FORWARDED_FOR']
                except Exception:
                    Log.error(
                        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                        + ': No key "HTTP_X_FORWARDED_FOR" in environ.'
                    )
                    remote_addr = environ['REMOTE_ADDR']

            remote_port = environ['REMOTE_PORT']
            Log.important(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': New livestream connection from "' + str(remote_addr)
                + ':' + str(remote_port) + '". Full environ: ' + str(environ)
            )
            client_socket = environ['wsgi.websocket']
            if type(client_socket) is WebSocket:
                try:
                    ClientWsHandler(
                        socket      = client_socket,
                        remote_addr = remote_addr,
                        remote_port = remote_port
                    ).handle_first_connection()

                    SubscriberList.mutex_client_subscribers_list.acquire()
                    subscriber = {
                        'socket': client_socket,
                        'remote_addr': remote_addr,
                        'remote_port': remote_port
                    }
                    SubscriberList.client_subscribers_list.append(subscriber)
                    Log.important(
                        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                        + ': Socket ' + str(remote_addr) + ':' + str(remote_port) + ' added to subscribers list.'
                    )
                except Exception as ex_add_client_socket:
                    Log.error(
                        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                        + ': Error adding client socket ' + str(remote_addr) + ':' + str(remote_port)
                        + ' to subscribers list: ' + str(ex_add_client_socket)
                        + '. Closing socket.'
                    )
                    client_socket.close()
                    return
                finally:
                    SubscriberList.mutex_client_subscribers_list.release()

                while True:
                    try:
                        message = client_socket.receive()
                        Log.info(
                            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Received: ' + str(message)
                        )
                        # TODO Do async handling here
                        if sys.version_info >= (3, 7, 0):
                            # asyncio.run(todo_handler())
                            pass
                        client_socket.send('Got your message ' + str(message))
                    except Exception as ex_socket:
                        Log.error(
                            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Error socket connection: ' + str(ex_socket)
                        )
                        break

                Log.important('Remote ' + str(remote_addr) + ':' + str(remote_port) + ' finished.')
            else:
                Log.error(
                    str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Wrong type, expecting WebSocket type, got "'
                    + str(type(client_socket)) + '" instead.'
                )
        else:
            Log.error(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Wrong request path "' + str(path) + '"'
            )
            return 'Wrong request path "' + str(path) + '". Start Response "' + str(start_response) + '"'
            # return app(environ, start_response)

    def __init__(
            self,
            socket,
            remote_addr,
            remote_port
    ):
        self.socket = socket
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.secret_subscriber_password = SubscriberSharedSecret.init_singleton_config()
        return

    def handle_first_connection(self):
        try:
            challenge = Authenticate.generate_challenge_string(n=100)
            Log.debug(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Sent challenge "' + str(challenge) + '" to ' + str(self.remote_addr)
                + ':' + str(self.remote_port)
            )
            self.socket.send(
                json.dumps({'challenge': challenge}, ensure_ascii=False).encode(ClientWsHandler.STR_ENCODING)
            )

            #
            # Expect something like
            #   {
            #     'id': anyone,
            #     'testChallenge':'abclkajfdas',
            #     'method':'challenge/totp-style'
            #   }
            #
            pkt = self.socket.receive()
            pkt_json = json.loads(pkt)

            method = 'challenge'
            subscriber_id = None
            str_test_challenge = None

            if 'method' in pkt_json.keys():
                method = pkt_json['method']

            if 'id' not in pkt_json.keys():
                raise Exception('Key "id" missing.')
            subscriber_id = pkt_json['id']
            shared_secret = self.secret_subscriber_password.get_config(param=subscriber_id)
            if shared_secret is None:
                raise Exception('Subscriber id "' + str(subscriber_id) + '" not in secret file.')

            if 'testChallenge' not in pkt_json.keys():
                raise Exception('Key "testChallenge" missing.')
            str_test_challenge = pkt_json['testChallenge']
            Log.info(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': From subscriber "' + str(subscriber_id)
                + '", received test challenge "' + str(str_test_challenge)
                + '", type ' + str(type(str_test_challenge))
            )

            # TODO Do async handling here
            if sys.version_info >= (3, 7, 0):
                # asyncio.run(todo_handler())
                pass

            authenticator_obj = Authenticate(
                    shared_secret  = shared_secret,
                    challenge      = challenge,
                    test_challenge = str_test_challenge
            )
            auth_result = False

            # Strong Authentication
            if method == 'totp-style':
                auth_result = authenticator_obj.verify_totp_style()
            elif method == 'totp':
                auth_result = authenticator_obj.verify_totp_otp()
            else:
                auth_result = authenticator_obj.verify()

            if auth_result == True:
                Log.info(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Authenticated connection from ' + str(self.remote_addr)
                    + ':' + str(self.remote_port) + '.'
                )
                self.socket.send('STRONG PASS Authenticated (Method "' + str(method) + '"): ' + str(str_test_challenge))
            else:
                self.socket.send('Иди отсюда')
                raise Exception('Wrong connect authentication "' + str(str_test_challenge) + '"')
        except Exception as ex:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                     + ': Connect error from socket ' + str(self.remote_addr)\
                     + ':' + str(self.remote_port) + '. Exception: ' + str(ex)
            raise Exception(errmsg)

