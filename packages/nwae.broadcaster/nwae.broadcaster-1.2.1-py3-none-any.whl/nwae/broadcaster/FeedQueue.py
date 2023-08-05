# -*- coding: utf-8 -*-

import queue


class FeedQueue:

    # This is a thread safe implementation, so no need to worry about multiple threads
    # https://docs.python.org/3/library/queue.html
    feed_queue = queue.Queue(
        maxsize = 10000
    )
