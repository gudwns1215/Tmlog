__all__ = ['Lg']

from time import time
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class Lg():
    def __init__(self, prefix="", timer=time):
        self.prefix = prefix
        self.timer = timer

        self.stack_time = defaultdict(lambda: 0)

        class Stacker():
            def __init__(s, key=""):
                s.timer = timer
                s.key = key
                
            def __enter__(s):
                s.st_time = s.timer()
                return s

            def __exit__(s, type, value, traceback):
                #Exception handling here
                s.ed_time = s.timer()
                self.stack_time[s.key] += s.ed_time - s.st_time

        self.stk = Stacker
        """
        stk usage
        with Tmlog() as tl:
            for i in range(10):
                with tl.stk("some codes"):
                    {some codes}
        """
        self.setup_logger()
    
    def setup_logger(self):
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('Tmlog.log', mode='a')
        ch = logging.StreamHandler()

        fh.setFormatter(logging.Formatter('%(asctime)s - (%(filename)s:%(lineno)d) - %(message)s'))
        ch.setFormatter(CustomStreamFormatter())

        logger.addHandler(fh)
        logger.addHandler(ch)

    def __enter__(self):
        self.total_st_time = self.timer()
        return self

    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.total_ed_time = self.timer()
        self.printer(self.prefix, self.total_ed_time - self.total_st_time)

        self.stack_time = dict(self.stack_time)
        # if self.stk called, print it.
        if self.stack_time:
            for k, v in self.stack_time.items():
                self.sub_printer(k, v)

    def printer(self, prefix, pasts):
        logger.info("[{}] time took: {:.2f}s".format(prefix, pasts))

    def sub_printer(self, key, pasts):
        logger.info("\t[{}] time took: {:.2f}s".format(key, pasts))

        
class CustomStreamFormatter(logging.Formatter):
    def __init__(self):
        grey = "\x1b[38;20m"
        green = '\x1b[33;32m'
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        format = "(%(filename)s:%(lineno)d) - %(message)s"
        
        self.FORMATS = {
            logging.DEBUG: grey + format + reset,
            logging.INFO: green + format + reset,
            logging.WARNING: yellow + format + reset,
            logging.ERROR: red + format + reset,
            logging.CRITICAL: bold_red + format + reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)