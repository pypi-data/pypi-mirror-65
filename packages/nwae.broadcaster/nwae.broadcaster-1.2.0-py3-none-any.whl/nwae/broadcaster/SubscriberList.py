# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
import threading


class SubscriberList:

    client_subscribers_list = []
    mutex_client_subscribers_list = threading.Lock()

