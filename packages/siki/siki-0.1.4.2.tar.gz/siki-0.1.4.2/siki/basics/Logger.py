# -*- coding: utf-8 -*-
# Author: Orlando Chen
# Create: May 31, 2018
# Modifi: Mar 18, 2018

from enum import Enum

from siki.basics import FileUtils as fileutil
from siki.basics import SystemUtils as sysutil
from siki.basics import Convert as convert
from siki.basics import TimeTicker as timetick
from siki.basics import Hashcode as hashcode
from siki.basics.Exceptions import NullPointerException, InvalidParamException


class Priority(Enum):
    INFO = 0
    DEBUG = 1
    WARNING = 2
    ERROR = 3


class Logger(object):


    def __init__(self, b_stdout = True, b_log = False, dir = None, file = None):
        self.m_bStdOut = b_stdout
        self.m_bUseLog = b_log
        if self.m_bUseLog:
            fileutil.mkdir(dir)
            self.m_file = file
            self.m_dir  = dir

    def _gen_logfile(self, dir, file):
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        
        #return fileutil.gen_path(dir, file, "log", timestamp)
        return fileutil.gen_filepath(dir, file, "log", timestamp)


    def _check_valid_file(self, dir, file):
        if dir is None or file is None:
            raise NullPointerException("Invalid operation, call init first")
        
        return self._gen_logfile(dir, file)


    def _priority_name(self, priority):
        if type(priority) is not Priority:
            raise InvalidParamException("'priority' must be an instance of Priority")
        if priority == Priority.INFO:
            return "INFO"
        elif priority == Priority.DEBUG:
            return "DEBUG"
        elif priority == Priority.WARNING:
            return "WARNING"
        elif priority == Priority.ERROR:
            return "ERROR"
        else:
            return "UNKNOWN"


    def file_path(self):
        return self._check_valid_file(self.m_dir, self.m_file)


    def message(self, priority, title = None, msg = None, exception = None):
        import traceback

        # check log is validate
        if self.m_bUseLog:
            f = self._check_valid_file(self.m_dir, self.m_file)

        errline = "{0} <{1}>".format(timetick.debug_msg_with_timestamp(), self._priority_name(priority))
        
        if title is not None:
            errline += "\t[{0}]".format(title)
    
        if msg is not None:
            errline += "\t{0}".format(msg)

        if sysutil.is_windows():
            errline += "\r\n"
        else:
            errline += "\n"

        if exception is not None:
            error = ''.join(traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__))
            errline += "{0}".format(error)
    
        if self.m_bUseLog:
            fileutil.write_file(f, convert.string_to_binary(errline), True)
        
        if self.m_bStdOut:
            print(errline)


    def _compute_base64(self, data: bytes):
        import base64
        
        # To be extra safe in python 3, encode text conditionally before concatenating with pad.
        if not isinstance(data, bytes):
            data = data.encode('utf-8')

        r = base64.b64encode(data)
        return convert.binary_to_string(r)


    def data_in_base64(self, priority, title: str, data: bytes):
        # check log is validate
        f = self._check_valid_file(self.m_dir, self.m_file)
        line = "{0} <{1}> [{2}]".format(timetick.debug_msg_with_timestamp(), self._priority_name(priority), title)

        if sysutil.is_windows():
            line += "\r\n    Data: {0}\r\n".format(self._compute_base64(data))
        else:
            line += "\n    Data: {0}\n".format(self._compute_base64(data))

        if self.m_bUseLog:
            fileutil.write_file(f, convert.string_to_binary(line), True)
        
        if self.m_bStdOut:
            print(line)


    def data_in_hashcode(self, priority, title: str, data: bytes):
        # check log is validate
        f = self._check_valid_file(self.m_dir, self.m_file)
        line = "{0} <{1}> [{2}]".format(timetick.debug_msg_with_timestamp(), self._priority_name(priority), title)

        if sysutil.is_windows():
            line += "\r\n    Data: {0}\r\n".format(hashcode.md5(data))
        else:
            line += "\n    Data: {0}\n".format(hashcode.md5(data))

        if self.m_bUseLog:
            fileutil.write_file(f, convert.string_to_binary(line), True)
        
        if self.m_bStdOut:
            print(line)



if __name__ == "__main__":
    log = Logger(False, True, "logs", "test")

    try:
        raise NullPointerException("invalid ptr")
    except Exception as e:
        log.message(Priority.INFO, "title", "check message", e)

    print(log.file_path())
    
    raw = fileutil.read_file("callback.py")
    log.data_in_base64(Priority.INFO, "data", raw)
    
    log.data_in_hashcode(Priority.ERROR, "hashcode", raw)