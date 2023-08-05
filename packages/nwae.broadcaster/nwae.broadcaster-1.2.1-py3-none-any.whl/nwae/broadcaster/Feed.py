# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import currentframe, getframeinfo
import re
from nwae.utils.ObjectPersistence import ObjectPersistence
from nwae.utils.Encode import Encode


class FeedObject:

    @staticmethod
    def __get_feed_cache_object_and_lock_file_path(
            feed_cache_folder,
            feed_id
    ):
        try:
            feed_id_base64 = Encode.encode_base64(
                s = str(feed_id)
            )
            obj_file_path = str(feed_cache_folder) + '/' + str(feed_id_base64) + '.cache'
            lock_file_path = obj_file_path + '.lock'

            return obj_file_path, lock_file_path
        except Exception as ex:
            Log.error(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error converting feed ID "' + str(feed_id)
                + '" to base 64. Exception: ' + str(ex)
            )
            return None, None


    @staticmethod
    def is_valid_feed_cache_object_file(
            obj_file_path
    ):
        m = re.match(
            pattern = '.*[.]cache$',
            string  = obj_file_path
        )
        if m:
            return True
        else:
            return False

    @staticmethod
    def get_feed_persistence_object(
            feed_cache_folder,
            feed_id
    ):
        obj_file_path, lock_file_path = FeedObject.__get_feed_cache_object_and_lock_file_path(
            feed_cache_folder = feed_cache_folder,
            feed_id           = feed_id
        )
        if obj_file_path is None:
            return None

        objper = ObjectPersistence(
            default_obj    = [],
            obj_file_path  = obj_file_path,
            lock_file_path = lock_file_path
        )
        return objper

    @staticmethod
    def get_feed_id_from_obj_file_path(
            obj_file_name
    ):
        try:
            feed_id_base64 = re.sub(pattern='.cache.*', repl='', string=str(obj_file_name))
            feed_id = Encode.decode_base64(
                s_base64 = feed_id_base64
            )
            return feed_id
        except Exception as ex:
            Log.error(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Error getting feed ID from file name "' + str(obj_file_name)
                + '". Exception: ' + str(ex)
            )
            return None

    def __init__(
            self,
            feed_dict_or_json,
            feed_id_key
    ):
        self.feed_dict = feed_dict_or_json
        self.feed_id_key = feed_id_key

        if type(self.feed_dict) is not dict:
            errmsg = \
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                + ': Wrong feed object type "' + str(type(self.feed_dict)) + '". Expected dict type.'
            Log.error(errmsg)
            raise Exception(errmsg)
        return

    def get_feed_id(
            self
    ):
        if self.feed_id_key not in self.feed_dict.keys():
            Log.warning(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Not caching feed. Missing key for feed ID "' + str(self.feed_id_key)
                + '" in feed: ' + str(self.feed_dict)
            )
            return None

        feed_id = self.feed_dict[self.feed_id_key]
        # Either None or empty string
        if not feed_id:
            Log.warning(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Not caching feed. Empty value for feed ID "' + str(feed_id)
                + '" in feed: ' + str(self.feed_dict)
            )
            return None

        return feed_id

