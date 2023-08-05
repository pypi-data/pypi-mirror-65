"""
fail the jenkins build if tests fail
"""

import os
from time import sleep


class Handler:
    @staticmethod
    def run(result, conf=None):
        print("DQ check failed, calling jenkins handler")
        # raise RuntimeError('TEST FAILED, STOPPING JENKINS!')
        # raise NameError('TESTS FAILED!')
        exit(1)
        print("YOU SHALL NOT SEE THIS MESSAGE!")


# Handler.run('result')
