# Copyright © 2020 Noel Kaczmarek
from datetime import datetime
import inspect
import gc


class Log:
    def __init__(self, file=None, *args, **kwargs):
        self.file = file
        self.log = []

        if file:
            self.init(file)

    def init(self, file):
        self.file = file

        with open(file, 'w') as f:
            pass

    @staticmethod
    def timestamp():
        return datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

    def makeLogEntry(self, msg, function, **kwargs):
        timestamp = self.timestamp()
        level = inspect.currentframe().f_back.f_code.co_name

        self.log.append({
            'timestamp': timestamp,
            'function': function,
            'level': level,
            'message': msg
        })

        if level == 'info' or level == 'warn':
            msg = '%s %s' % (timestamp, msg)
        else:
            msg = '%s %s in function \'%s\': %s' % (timestamp, level, function, msg)

        if kwargs.get('verbose', True):
            print(msg)

        msg += '\n'

        if not self.file:
            print('You cannot log without setting a log file first!')

        with open(self.file, 'a') as f:
            f.write(msg)
            f.close()

    def info(self, msg, **kwargs):
        function = inspect.currentframe().f_back.f_code.co_name
        self.makeLogEntry(msg, function, verbose=kwargs.get('verbose', True))

    def warn(self, msg, **kwargs):
        function = inspect.currentframe().f_back.f_code.co_name
        self.makeLogEntry(msg, function, verbose=kwargs.get('verbose', True))

    def error(self, msg, **kwargs):
        function = inspect.currentframe().f_back.f_code.co_name
        self.makeLogEntry(msg, function, verbose=kwargs.get('verbose', True))

    def critical(self, msg, **kwargs):
        function = inspect.currentframe().f_back.f_code.co_name
        self.makeLogEntry(msg, function, verbose=kwargs.get('verbose', True))

        gc.collect()
        exit()
