#!/usr/bin/env python2.7

import unittest
import sys


class Suite(object):
    def __init__(self, pattern):
        self.suite = unittest.TestLoader().discover('test',
                                                    pattern=pattern)

    def __call__(self):
        result = unittest.TextTestRunner(verbosity=2).run(self.suite)
        if result.errors or result.failures:
            return 1
        return 0


suites = {'unit': Suite('*_test.py'),
          'acceptance': Suite('*_acceptance.py')}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage:"
        print "\trunner.py [unit|acceptance]"
    suite = sys.argv[1]
    sys.exit(suites[sys.argv[1]]())
