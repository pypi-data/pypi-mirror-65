"""
this is a test handler for the unit test - test_ham_run
"""

from datacoco_core import Logger

LOG = Logger()


class SqlCompare(object):
    """

    """

    def __init__(self, test_conf):
        """

        :param test_conf:
        :return:
        """
        self.test_conf = test_conf

    def setup(self, CONF):
        print("Setting up...")
        # pass

        return self

    def run(self):
        status = "success"

        detail = {
            "status": status,
            "test": "sample test",
            "result_a": "any result a",
            "result_b": "any result b",
            "diff": 0,
            "test_conf": self.test_conf,
        }

        return status, detail
