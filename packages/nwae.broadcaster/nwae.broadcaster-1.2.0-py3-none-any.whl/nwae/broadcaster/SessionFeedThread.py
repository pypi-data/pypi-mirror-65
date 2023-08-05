# -*- coding: utf-8 -*-

import threading
from nwae.utils.Log import Log
from inspect import currentframe, getframeinfo
from nwae.utils.ObjectPersistence import ObjectPersistence
from datetime import datetime
import nwae.utils.Profiling as prf
import os
import time
import re
from nwae.broadcaster.Feed import FeedObject
import datetime as dt


#
# Return session feed IDs from cache folder
# TODO Still not working
#
class SessionFeedThread(threading.Thread):

    SESSION_FEED_CONNECTED_TIME = 'connectedTime'
    SESSION_FEED_LAST_ACTIVE_TIME = 'lastActiveTime'

    SESSION_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(
            self,
            # We keep the session feeds in a file, not memory
            cache_file_path,
            lock_file_path,
            # Where all the feed resides
            feed_cache_folder,
            # Key to identify the unique key of the feed
            feed_id_key,
            feed_datetime_key,
            timeout_secs = 10*60
    ):
        super().__init__()
        # Keep all the live feed sessions (last activity seen within <timeout_secs>
        self.session_cache = ObjectPersistence(
            default_obj    = {},
            obj_file_path  = cache_file_path,
            lock_file_path = lock_file_path
        )
        self.feed_cache_folder = feed_cache_folder
        if not os.path.exists(self.feed_cache_folder):
            raise Exception(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Feed cache folder "' + str(self.feed_cache_folder)
                + '" does not exist!'
            )
        self.feed_id_key = feed_id_key
        self.feed_datetime_key = feed_datetime_key

        self.timeout_secs = timeout_secs
        self.stoprequest = threading.Event()
        self.__mutex = threading.Lock()
        try:
            self.__cleanup_old_feeds()
        except Exception as ex:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                + ': Feed cleanup exception: ' + str(ex)
            )
        return

    def join(self, timeout=None):
        Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Join called..'
        )
        self.stoprequest.set()
        super().join(timeout=timeout)

    def __sanity_check_feed(
            self,
            feed_obj
    ):
        if type(feed_obj) is not dict:
            errmsg = \
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                + ': Wrong feed object type "' + str(type(feed_obj)) + '". Expected dict type.'
            Log.error(errmsg)
            return False
        else:
            return True

    def __update_persistent_object(
            self,
            cache_obj,
            comment = None
    ):
        if not self.session_cache.update_persistent_object(new_obj=cache_obj):
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error updating session cache: ' + str(comment)
            )
        else:
            Log.info(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Successfully updated session cache: ' + str(comment)
            )

    def __cleanup_old_feeds(self):
        cache_obj = self.session_cache.read_persistent_object()

        expired_feed_ids = []
        Log.debug(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Clean Old Feeds from ' + str(cache_obj)
        )
        for feed_obj in cache_obj.values():
            feed_id = feed_obj[self.feed_id_key]
            last_updated = feed_obj[SessionFeedThread.SESSION_FEED_LAST_ACTIVE_TIME]
            dif_secs = prf.Profiling.get_time_dif(
                start    = dt.datetime.strptime(
                    last_updated,
                    SessionFeedThread.SESSION_DATETIME_FORMAT
                ),
                stop     = datetime.now(),
                decimals = 1
            )
            Log.debug(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Feed ID "' + str(feed_id) + '" last activity ' + str(dif_secs) + ' secs ago.'
            )
            if dif_secs > self.timeout_secs:
                Log.important(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Put feed ID "' + str(feed_id) + '", last updated "' + str(last_updated)
                    + '" for removal from session chats.'
                )
                expired_feed_ids.append(feed_id)
            else:
                Log.debug(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ' Feed ID "' + str(feed_id) + '" OK, last active time "' + str(last_updated)
                    + '" is within ' + str(dif_secs) + 's from current time.'
                )

        try:
            feed_items_to_remove = {}
            for feed_id in expired_feed_ids:
                feed_items_to_remove[feed_id] = None
                Log.important(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Schedule feed ID "' + str(feed_id) + '" for removal from session chats.'
                )
            self.session_cache.atomic_update(
                new_items = feed_items_to_remove,
                mode      = ObjectPersistence.ATOMIC_UPDATE_MODE_REMOVE,
                max_wait_time_secs = 5.0
            )
        except Exception as ex:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Exception cleanup old feeds: ' + str(ex)
            )

    def add_or_update_feed(
            self,
            feed_id,
            feed_obj
    ):
        if not self.__sanity_check_feed(feed_obj = feed_obj):
            Log.warning(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Wrong feed object type "' + str(type(feed_obj)) + '", feed object: ' + str(feed_obj)
            )
            return False

        try:
            self.session_cache.atomic_update(
                new_items = {feed_id: feed_obj},
                mode      = ObjectPersistence.ATOMIC_UPDATE_MODE_ADD,
                max_wait_time_secs = 5.0
            )
        except Exception as ex:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error adding feed "' + str(feed_id) + '" into session cache.'
            )

    def remove_feed(
            self,
            feed_id,
            feed_obj
    ):
        if not self.__sanity_check_feed(feed_obj = feed_obj):
            return False

        # TODO Put this in separate thread
        self.__cleanup_old_feeds()

        try:
            self.session_cache.atomic_update(
                new_items = {feed_id: feed_obj},
                mode      = ObjectPersistence.ATOMIC_UPDATE_MODE_REMOVE,
                max_wait_time_secs = 5.0
            )
        except Exception as ex:
            Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error removing feed "' + str(feed_id) + '" from session cache.'
            )

    def get_sessions_active(
            self
    ):
        return self.session_cache.read_persistent_object(
            max_wait_time_secs = 1
        )

    def run(self):
        while True:
            if self.stoprequest.isSet():
                Log.critical(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Thread ' + str(threading.get_ident()) + ' received stop request...'
                )
                break

            try:
                self.__cleanup_old_feeds()

                # Loop feed cache folder
                feed_cache_files = []
                for f in os.listdir(self.feed_cache_folder):
                    if not FeedObject.is_valid_feed_cache_object_file(
                            obj_file_path = f
                    ):
                        Log.debugdebug(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': File "' + str(f) + '" not a valid feed persistence file'
                        )
                    else:
                        feed_cache_files.append(f)

                Log.debug(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Checking Feed cache files: ' + str(feed_cache_files)
                )

                for i in range(len(feed_cache_files)):
                    f = feed_cache_files[i]

                    feed_id = FeedObject.get_feed_id_from_obj_file_path(
                        obj_file_name = f
                    )
                    if feed_id is None:
                        continue
                    obj_file_path = self.feed_cache_folder + '/' + f

                    Log.debug(
                        str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                        + ': Loading feed cache from file ' + str(i) + '. ' + str(obj_file_path)
                    )

                    feed_obj = None
                    try:
                        feed_obj_per = FeedObject.get_feed_persistence_object(
                            feed_cache_folder = self.feed_cache_folder,
                            feed_id           = feed_id
                        )
                        if feed_obj_per is None:
                            raise Exception('Object persistence file is None')

                        feed_obj = feed_obj_per.read_persistent_object(
                            max_wait_time_secs = 1
                        )
                        Log.debug(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Feed object serialized from file "' + str(obj_file_path)
                            + '": ' + str(feed_obj)
                        )
                    except Exception as ex:
                        Log.error(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Error deserializing from file "' + str(obj_file_path) + '"'
                        )
                        continue

                    if type(feed_obj) not in [tuple, list]:
                        Log.warning(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Feed Object is None or wrong type "' + str(type(feed_obj))
                            + '" from file "' + str(f)
                        )
                        continue
                    if len(feed_obj) == 0:
                        continue

                    # Get last updated time
                    connect_datetime = dt.datetime(year=8000, month=1, day=1)
                    last_datetime = dt.datetime(year=2000, month=1, day=1)
                    for fd in feed_obj:
                        if self.feed_datetime_key not in fd.keys():
                            Log.debug(
                                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                                + ': Missing datetime key "' + str(self.feed_datetime_key)
                                + '" in feed line ' + str(fd)
                            )
                            # Ignore line with no datetime key
                            continue

                        tmp_datetime = dt.datetime.strptime(
                            fd[self.feed_datetime_key],
                            SessionFeedThread.SESSION_DATETIME_FORMAT
                        )
                        if tmp_datetime > last_datetime:
                            last_datetime = tmp_datetime
                        if tmp_datetime < connect_datetime:
                            connect_datetime = tmp_datetime

                    interval_no_act = dt.datetime.now() - last_datetime

                    # If not in our session cache
                    if interval_no_act.total_seconds() < self.timeout_secs:
                        Log.debug(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Checking Feed "' + str(feed_id)
                            + '" connected time: ' + str(connect_datetime)
                            + '" last updated: ' + str(last_datetime)
                            + ', secs no activity: ' + str(interval_no_act.total_seconds())
                        )
                        session_per_obj = self.session_cache.read_persistent_object(
                            max_wait_time_secs = 1
                        )
                        connect_datetime_string = connect_datetime.strftime(
                            SessionFeedThread.SESSION_DATETIME_FORMAT
                        )
                        last_active_datetime_string = last_datetime.strftime(
                            SessionFeedThread.SESSION_DATETIME_FORMAT
                        )
                        need_to_update = False
                        if feed_id not in session_per_obj.keys():
                            need_to_update = True
                        else:
                            if session_per_obj[feed_id][SessionFeedThread.SESSION_FEED_LAST_ACTIVE_TIME] != last_active_datetime_string:
                                need_to_update = True
                        # Add or update the session
                        if need_to_update:
                            Log.info(
                                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                                + ': Updating feed "' + str(feed_id)
                                + '" connected time: ' + str(connect_datetime)
                                + '" last updated: ' + str(last_datetime)
                                + ', secs no activity: ' + str(interval_no_act.total_seconds())
                            )
                            self.add_or_update_feed(
                                feed_id = feed_id,
                                feed_obj = {
                                    self.feed_id_key: feed_id,
                                    SessionFeedThread.SESSION_FEED_CONNECTED_TIME: connect_datetime_string,
                                    SessionFeedThread.SESSION_FEED_LAST_ACTIVE_TIME: last_active_datetime_string
                                }
                            )
                    else:
                        per_obj = self.session_cache.read_persistent_object(
                            max_wait_time_secs = 1
                        )
                        if feed_id in per_obj.keys():
                            feed_obj = per_obj[feed_id]
                            self.remove_feed(
                                feed_id = feed_id,
                                feed_obj = feed_obj
                            )
            except Exception as ex_session_thread:
                Log.critical(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Session thread error: ' + str(ex_session_thread)
                )

            time.sleep(5)


