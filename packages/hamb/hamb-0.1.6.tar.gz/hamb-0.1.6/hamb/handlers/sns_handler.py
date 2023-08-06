"""
sns handler - future use
"""

import logging, logging.handlers


class Handler(object):
    def __init__(self, config=None):
        self.config = config

    def run(self, result, conf):
        # just a shell for now
        print("send sns")

    def setup(self):
        return self