# -*- coding: utf-8 -*-

import flask
import sys
import os
import nwae.broadcaster.config.Config as cf
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
from nwae.broadcaster.subscriber.SubscriberSharedSecret import SubscriberSharedSecret
from nwae.broadcaster.SubscriberList import SubscriberList
from nwae.broadcaster.FeedQueue import FeedQueue
from nwae.broadcaster.AggregateServer import AggregateServerThread
from nwae.broadcaster.BroadcastThread import BroadcastThread
from nwae.broadcaster.ClientWsHandler import ClientWsHandler
from nwae.broadcaster.CleanupThread import CleanupThread
from nwae.broadcaster.SessionFeedThread import SessionFeedThread
import signal


#
# Push & Pull Feed
# This API allows all feed processes to send feed to one place.
# It also allows retrieval (cached for some time)
#
app = flask.Flask(__name__)


#
# Feed aggregated by AggregateServer will be re-broadcasted by Broadcast Server
#
def Start_Broadcast_Server():
    obj = BroadcastServer()
    return obj

#
# Rebroadcasts feed aggregated in AggregateServer
#
class BroadcastServer:

    DEFAULT_CONFIG_FILE = '/usr/local/git/nwae/nwae.broadcaster/app.data/config/broadcaster.cf'

    #
    # Startup Initialization. Read configurations from command line.
    # The first thing we do is to process command line parameters, account, port, etc.
    # This function should be called first thing at __init__()
    #
    def __init_command_line_parameters(self):
        configfile = None
        try:
            #
            # Run like '/usr/local/bin/python3.6 -m nwae.broadcaster.BroadcastServer configfile=... port=...'
            #
            # Default values
            command_line_params = {
                cf.Config.PARAM_CONFIGFILE: None,
                cf.Config.PARAM_PORT_BROADCASTER: None
            }
            args = sys.argv

            for arg in args:
                arg_split = arg.split('=')
                if len(arg_split) == 2:
                    param = arg_split[0].lower()
                    value = arg_split[1]
                    if param in list(command_line_params.keys()):
                        command_line_params[param] = value

            return command_line_params
        except Exception as ex:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                     + ': Error reading app config file "' + str(configfile)\
                     + '". Exception message ' + str(ex)
            Log.critical(errmsg)
            raise Exception(errmsg)

    def __init__(self):
        cmdline_params = self.__init_command_line_parameters()
        self.config = cf.Config.get_cmdline_params_and_init_config_singleton(
            Derived_Class = cf.Config,
            default_config_file = BroadcastServer.DEFAULT_CONFIG_FILE
        )

        #
        # Secret config of id/password must exist
        #
        secret_config_file_path = self.config.get_config(param=cf.Config.PARAM_SHARED_SECRET_FILE)
        if not os.path.isfile(secret_config_file_path):
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Secret config of id/password file "' + str(secret_config_file_path)
                + '" not exist!'
            )
        Log.important(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Secret id/password file path ok "' + str(secret_config_file_path) + '".'
        )
        SubscriberSharedSecret.singleton_config_file_path = secret_config_file_path
        SubscriberSharedSecret.init_singleton_config()

        #
        # Overwrite config file port if on command line, port is specified
        #
        if cmdline_params[cf.Config.PARAM_PORT_BROADCASTER] is not None:
            Log.important(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Overwriting port in config file "'
                + str(self.config.get_config(param=cf.Config.PARAM_PORT_BROADCASTER))
                + '" with port specified on command line as "'
                + str(cmdline_params[cf.Config.PARAM_PORT_BROADCASTER]) + '".'
            )
            self.config.param_value[cf.Config.PARAM_PORT_BROADCASTER] = cmdline_params[cf.Config.PARAM_PORT_BROADCASTER]

        # For gunicorn to access, and will never change without a restart
        self.port = int(self.config.get_config(param=cf.Config.PARAM_PORT_BROADCASTER))
        self.host = '0.0.0.0'

        #
        # Start Cleanup Thread in background
        #   The aggregate server keeps the feeds in separate cache files by feed ID,
        #   this cleanup thread will delete files older than <max_age_secs>
        #
        self.cleanup_thread = CleanupThread(
            cleanup_folder = self.config.get_config(param=cf.Config.PARAM_FEED_CACHE_FOLDER),
            files_regex    = '.*.cache$',
            # 30 mins, then we clean
            max_age_secs   = 30*60
        )
        self.cleanup_thread.start()

        #
        # Start Session Thread in background
        #   This thread checks the feed cache files, and keeps a record of all feed IDs that
        #   is still active, with last activity less than <timeout_secs> seconds
        #
        ses_feed_cache_folder = self.config.get_config(param=cf.Config.PARAM_SESSION_FEED_CACHE_FOLDER)
        self.session_feed_thread = SessionFeedThread(
            cache_file_path   = ses_feed_cache_folder + '/session.feed.cache',
            lock_file_path    = ses_feed_cache_folder + '/session.feed.cache.lock',
            feed_cache_folder = self.config.get_config(param=cf.Config.PARAM_FEED_CACHE_FOLDER),
            feed_id_key       = self.config.get_config(param=cf.Config.PARAM_FEED_ID_KEY),
            feed_datetime_key = self.config.get_config(param=cf.Config.PARAM_FEED_DATETIME_KEY),
            timeout_secs      = 10*60
        )
        self.session_feed_thread.start()

        #
        # Broadcast Thread
        #   This thread handles the web socket connections and broadcast on those sockets
        #
        self.broadcast_thread = BroadcastThread(
            client_subscribers_list = SubscriberList.client_subscribers_list,
            mutex_client_subscribers_list = SubscriberList.mutex_client_subscribers_list,
            feed_queue = FeedQueue.feed_queue
        )
        self.broadcast_thread.start()
        Log.important(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Broadcast Thread starting in the background..'
        )

        #
        # Start Chat Aggregator in background
        #   This thread runs the Feed Push/Pull Rest API
        #
        self.agg_server_thread = AggregateServerThread(
            flask_app      = app,
            config         = self.config,
            session_thread = self.session_feed_thread
        )
        self.agg_server_thread.start()
        Log.important(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Aggregator Server starting in the background..'
        )

        # register the signals to be caught
        signal.signal(signal.SIGHUP, self.signal_received)
        signal.signal(signal.SIGINT, self.signal_received)
        # signal.signal(signal.SIGQUIT, receiveSignal)
        # signal.signal(signal.SIGILL, receiveSignal)
        # signal.signal(signal.SIGTRAP, receiveSignal)
        # signal.signal(signal.SIGABRT, receiveSignal)
        # signal.signal(signal.SIGBUS, receiveSignal)
        # signal.signal(signal.SIGFPE, receiveSignal)
        # # signal.signal(signal.SIGKILL, receiveSignal)
        # signal.signal(signal.SIGUSR1, receiveSignal)
        # signal.signal(signal.SIGSEGV, receiveSignal)
        # signal.signal(signal.SIGUSR2, receiveSignal)
        # signal.signal(signal.SIGPIPE, receiveSignal)
        # signal.signal(signal.SIGALRM, receiveSignal)
        # signal.signal(signal.SIGTERM, receiveSignal)
        # # register the signal to be ignored
        # signal.signal(signal.SIGINT, signal.SIG_IGN)

        return

    def signal_received(
            self,
            signal_number,
            frame
    ):
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Received signal ' + str(signal_number) + '..'
        )

        self.agg_server_thread.join()
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Aggregate server thread joined'
        )

        self.broadcast_thread.join()
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Broadcast thread joined'
        )

        self.cleanup_thread.join()
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Cleanup thread joined'
        )

        self.session_feed_thread.join()
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Session feed thread joined'
        )

        return

    def run(self):
        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Starting Broadcast Server on ' + str(self.host) + ':' + str(self.port)
        )
        server = WSGIServer(
            (self.host, self.port),
            ClientWsHandler.ConnectionHandler,
            handler_class = WebSocketHandler
        )
        server.serve_forever()


if __name__ == '__main__':
    # One time initialization applies to all modules
    Log.LOGLEVEL = Log.LOG_LEVEL_INFO
    print(str(__name__) + ': Using log file path "' + str(Log.LOGFILE))
    Log.DEBUG_PRINT_ALL_TO_SCREEN = True

    svr = Start_Broadcast_Server()
    svr.run()
