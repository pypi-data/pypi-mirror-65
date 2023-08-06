"""
fail the jenkins build if tests fail
"""

import os


class Handler(object):
    def __init__(self, config=None):
        self.config = config

    def run(self, result, conf):
        print("DQ check failed, calling jenkins handler")
        # raise RuntimeError('TEST FAILED, STOPPING JENKINS!')
        # raise NameError('TESTS FAILED!')
        exit(1)

    def setup(self):
        return self
