__all__ = ['Lg']

from time import time
from collections import defaultdict

class Lg():
    def __init__(self, prefix="", timer=time, print_fn=print):
        self.prefix = prefix
        self.timer = timer
        self.print_fn = print_fn

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
        self.print_fn("[{}] time pasts: {:.2f} seconds".format(prefix, pasts))

    def sub_printer(self, key, pasts):
        self.print_fn("\t{}: {:.2f} sec".format(key, pasts))