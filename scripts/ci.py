#!/usr/bin/env python2.7

import sys
from collections import namedtuple
from subprocess import call


Task = namedtuple('Task', 'run name')


def sh(*commands):
    results = []
    for command in commands:
        print command
        results.append(call(command.split()))
    return max(results)


tasks = iter([Task(name='clean',
                   run=lambda: sh('find . -name *.pyc -delete')),
              Task(name='lint',
                   run=lambda: sh('flake8 ./test ./xcell ./scripts')),
              Task(name='unit',
                   run=lambda: sh('./scripts/runner.py unit')),
              Task(name='acceptance',
                   run=lambda: sh('./scripts/runner.py acceptance'))])


if __name__ == '__main__':
    current_status_code = 0
    current = None
    while current_status_code == 0:
        print 'PASS'
        try:
            current = tasks.next()
        except StopIteration:
            break
        print current.name
        current_status_code = current.run()
    if current_status_code:
        print "FAIL"
    sys.exit(current_status_code)
