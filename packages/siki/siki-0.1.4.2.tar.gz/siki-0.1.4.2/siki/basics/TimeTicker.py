# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Created: May 09, 2018
# LastChg: Mar 11, 2020

MS_PER_SECOND = 1000
MS_PER_MINUTE = 60000
MS_PER_HOUR = 3600000
MS_PER_DAY = 86400000

def debug_msg_with_timestamp(strMessage = None):
    """
    return to caller a string message with timestamp for debug purpose

    @Args:
    * [strMessage] message to display, if none, the returning will just 
        only a timestamp of the format YYYY-mm-dd HH:MM:SS.ms

    @Returns:
    * [str] returning a string with timestamp
    """
    import datetime
    if strMessage is None:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    else:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return "{0} {1}".format(timestamp, strMessage)


def time_since1970():
    """
    Returning a decimal number with couting the last seconds since 1970

    @Returns:
    * [float] 
    """
    import time
    return time.time()


def time_now_foramt(format: str):
    """
    Returning a formatted string of time

    @Args:
    * [format] str, something like %Y-%m-%d %H:%M:%S.%f

    @Returns:
    * [str] the formatted string of time
    """
    import datetime
    return datetime.datetime.now().strftime(format)


