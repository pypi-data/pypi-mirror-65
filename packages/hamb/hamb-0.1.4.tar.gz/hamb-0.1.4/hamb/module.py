"""
this will be the main entry point to the program,
will probably end up being a flask web service, with a basic UI
"""
import os
import sys
import argparse

from hamb.config_wrapper import ConfigWrapper
from hamb.ham_run_utility import TestEngine, HandlerEngine


def main(args):

    parser = argparse.ArgumentParser()

    parser = ConfigWrapper.parse(parser)
    args = parser.parse_args(args)

    manifest = args.manifest
    parameters = args.parameters
    db_log_table = args.db_log_table

    config = ConfigWrapper.process_config(args)

    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, "startup_banner.txt"), "r") as myfile:
        data = myfile.read()
        print(data)

    result = TestEngine().run(
        manifest=manifest,
        config=config,
        db_log_table=db_log_table,
        params=parameters,
    )
    HandlerEngine().run(manifest=manifest, result=result, config=config)


if __name__ == "__main__":
    main(sys.argv[1:])
