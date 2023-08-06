import time
import random
from itertools import count, chain, repeat
try:
    from itertools import izip
except ImportError:
    izip = zip
from functools import partial
import math

__author__ = 'paul'
__all__ = ["exponential_backoff", "convert_bytes", "convert_bytes_10"]

class exponential_backoff(object):
    def __init__(self, max_retries=None):
        self.max_retries = max_retries
        self.reset()

    def reset(self):
        self.iter = iter(self.__get_iter())

    def backoff(self):
        try:
            next(self.iter)
            return True
        except StopIteration:
            return False

    def __iter__(self):
        """
        For use in for loop

        >>> for retry in exponential_backoff(3):
        ...     print "do something",
        ...     if retry:
        ...         print "retry no.%i" % retry
        ...     else:
        ...         print
        ...
        do something
        do something retry no.1
        do something retry no.2
        do something retry no.3
        """
        return self.iter

    def __get_iter(self):
        counter = count() if self.max_retries is None else iter(xrange(max(self.max_retries, 0) + 1))
        sleep_counter = chain(xrange(6), repeat(6))
        yield counter.next()
        for i, sleep_val in izip(counter, sleep_counter):
            time.sleep((random.randrange(2 ** sleep_val, 2 ** (sleep_val + 1)) - 0.5) + random.random())
            yield i

    def __nonzero__(self):
        """
        For use in a while loop

        >>> backoff = exponential_backoff(3)
        >>> while backoff:
        ...     print "do something"
        ...
        do something
        do something
        do something
        do something
        """
        return self.backoff()


def convert_bytes(quantity, round_start=2, round_precision=2, multiple=1024, smart_trim=False, no_spaces=False,
                  suffix_list=("B",) + tuple(letter + "B" for letter in "KMGTPEZY")):
    try:
        quantity = float(quantity)
    except ValueError:
        quantity = 0
    base = "%s%s" if no_spaces else "%s %s"

    last_suffix = suffix_list[-1]

    for pos, suffix in enumerate(suffix_list):
        if abs(quantity) < multiple or suffix == last_suffix:
            if pos < round_start:
                suff_str = int(math.ceil(quantity))
            else:
                suff_str = "%%.%if" % round_precision % quantity
                if smart_trim and round_precision:
                    suff_str = suff_str.rstrip("0").rstrip(".")
            return base % (suff_str, suffix)
        else:
            quantity /= multiple

convert_bytes_10 = partial(convert_bytes, multiple=1000)