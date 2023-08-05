import os
import yaml
import pandas as pd
import uuid
from pprint import pprint
from datetime import datetime
from datacoco_core import Logger
from collections import OrderedDict
from sqlalchemy import create_engine
from pathlib import Path

LOG = Logger()
KEY_PREFIX = "dq"


class HandlerEngine(object):
    """
    This class is used for sending results to external providers
    """

    def run(self, manifest: str, config: dict, result: dict):
        """
        in this step we read test_result
        import and run appropriate handler(s)
        :return:
        """
        LOG.l("\n---------------------------\nhandlers")
        level = result["summary"]["status"]
        LOG.l("handler level: " + level)
        h_config = self.get_handler_config(manifest, level)

        print(
            "\n---------------------------\noverall results for: "
            + manifest
            + "\n"
        )
        pprint(result["START SUMMARY"])
        print("SUMMARY:")
        pprint(result["summary"])
        print("\n" + "SUCCESSES:" + "\n")
        pprint(result["success detail"])
        print("FAILS:" + "\n")
        pprint(result["fail detail"])
        print("\n")
        pprint(result["table"])
        print("\n")

        # service specific handlers
        for handler in h_config:
            print(f"handler: {handler}")
            LOG.l("executing handler: " + list(handler.keys())[0])
            test_module = f"hamb.handlers.{list(handler.keys())[0]}"
            print(test_module)
            mod = __import__(test_module, fromlist=["Handler"])
            class_ = getattr(mod, "Handler")
            class_(config).setup().run(result, list(handler.values())[0])

    @staticmethod
    def get_handler_config(service, level):
        """

        :param manifest:
        :return:
        """

        # Get current working dir and fine manifest folder
        cwd = os.getcwd()
        # If file is not found, check hambot main manifest directory
        file = Path(os.path.join(cwd, f"services.yaml")).is_file()
        if not file:
            script_dir = os.path.dirname(__file__)
            file_location = os.path.join(script_dir, f"config/services.yaml")
        else:
            file_location = os.path.join(cwd, f"services.yaml")

        with open(file_location, "r") as services_yaml:
            try:
                obj = yaml.safe_load(services_yaml)
            except Exception as e:
                LOG.l_exception(f"issue parsing yaml: {e}")
                exit(1)
            if service in obj:
                handler_config = obj[service][level]
            else:
                handler_config = obj["default"][level]
        return handler_config


class TestEngine(object):
    """
    main entry point for ham_run
    """

    def run(self, manifest: str, config: dict, params=None, db_log_table=None):
        """
        this will be the core data model
        result= {
            'START SUMMARY': [],
            'summary': {},
            'new output': {},
            'success detail': [],
            'fail detail': []
        }

        :param args:
        :return:
        """
        status = None
        passed_cnt = 0
        warning_cnt = 0
        failed_cnt = 0

        result = OrderedDict()
        result["START SUMMARY"] = (
            "**************************************\
            ***************************************\
            ***************************************\
            ***************************************\
            ************************"
            "**************************************\
            ***************************************\
            ***************************************\
            ***************************************\
            ************************"
        )
        result["table"] = {}
        result["summary"] = {}
        result["fail detail"] = []
        result["success detail"] = []

        params = self.process_params(params)

        test_config = self.manifest_reader(manifest)
        job = []
        stat = []
        diff = []
        for test, test_conf in test_config.items():
            test_module = f'hamb.{test_conf["type"].lower()}'
            mod = __import__(test_module, fromlist=["SqlCompare"])
            try:
                class_ = getattr(mod, "SqlCompare")
            except Exception as e:
                LOG.l_exception(
                    f"module not present or issue in module import: {e}"
                )
                exit(1)

            if params is None:
                status, detail = class_(test_conf).setup(config).run()
            else:
                try:
                    status, detail = class_(test_conf, params).run()
                except Exception as e:
                    print(str(e))
                    exit(1)

            if status == "success":
                passed_cnt += 1
            elif status == "warning":
                warning_cnt += 1
            else:
                failed_cnt += 1

            if status == "success":
                result["success detail"].insert(0, detail)
                diff.append(" ")
            elif status == "warning":
                result["success detail"].append(detail)
                diff.append(detail["diff"])
            else:
                result["fail detail"].append(detail)
                diff.append(detail["diff"])

            job.append(detail["test"])
            stat.append(detail["status"])
            LOG.l(status)
            LOG.l(detail)

            # Save execution results to db
            if db_log_table is not None:
                self.save_db_log(
                    db_connection=config["hambot"]["database"],
                    db_env=config["hambot"]["environment"],
                    db_table=db_log_table,
                    manifest=manifest,
                    manifest_config=test_conf,
                    test=test,
                    status=status,
                    detail=detail,
                )

        if failed_cnt > 0:
            overall_status = "failure"
        elif warning_cnt > 0:
            overall_status = "warning"
        else:
            overall_status = "success"

        result["summary"] = {
            "status": overall_status,
            "failed_count": failed_cnt,
            "warning_cnt": warning_cnt,
            "passed_cnt": passed_cnt,
            "exec_time": str(datetime.now()),
            "manifest": manifest,
        }
        table = {"Job": job, "Status": stat, "Diff": diff}
        result["table"] = pd.DataFrame(
            data=table, columns=("Job", "Status", "Diff")
        )

        return result

    def process_params(self, param_string):
        if param_string is None:
            return

        paramDict = {}
        keyValPairs = param_string.split(",")
        for pair in keyValPairs:
            keyVal = pair.split(":")
            paramDict[keyVal[0]] = keyVal[1]
        return paramDict

    @staticmethod
    def save_db_log(
        db_connection: str,
        db_env: str,
        db_table: str,
        manifest: str,
        test,
        status,
        manifest_config,
        detail,
    ):
        # add to database

        engine = create_engine(db_connection)
        idnum = uuid.uuid1()

        try:
            statement = """INSERT INTO {table}
            (manifest, test, status, source_connection, "source count",
            target_connection, "target count", diff, warning_threshold,
            failure_threshold, environment, created_time, uuid)
            VALUES ('{manifest}', '{test}', '{status}', '{conn_a}', '{result_a}', '{conn_b}', '{result_b}', '{diff}', '{warning}', '{failure}', '{env}', '{datetime}', '{id}')""".format(
                table=db_table,
                manifest=manifest,
                test=test,
                status=status,
                conn_a=manifest_config["conn_a"],
                result_a=", ".join(str(d) for d in detail["result_a"])
                if isinstance(detail["result_a"], list)
                else detail["result_a"],
                conn_b=manifest_config["conn_b"],
                result_b=", ".join(str(d) for d in detail["result_b"])
                if isinstance(detail["result_b"], list)
                else detail["result_b"],
                diff=detail["diff"] if detail["diff"] is not None else 0,
                warning=manifest_config["warning_threshold"],
                failure=manifest_config["failure_threshold"],
                env=db_env,
                datetime=datetime.now(),
                id=idnum,
            )
            engine.execute(statement)
        except Exception as e:
            print(f"cannot write results to database: {e}")

    @staticmethod
    def manifest_reader(manifest, file_location=None):
        """

        :param manifest
        :return: dict
        """
        manifest_path, manifest_name = os.path.split(manifest)
        if manifest_path is None:
            file_path = f"{manifest_path}/{manifest_name}.yaml"
            # Check if file exists in given manifest path
            file = Path(file_path).is_file()
            if not file:
                e = f"{file_path} not found."
                raise RuntimeError(e)
            file_location = file_path
        else:
            # Get current working dir and fine manifest folder
            cwd = os.getcwd()
            # If file is not found, check hambot main manifest directory
            file = Path(
                os.path.join(cwd, f"manifests/{manifest_name}.yaml")
            ).is_file()
            if not file:
                script_dir = os.path.dirname(__file__)
                file_location = os.path.join(
                    script_dir, f"manifests/{manifest_name}.yaml"
                )
            else:
                file_location = os.path.join(
                    cwd, f"manifests/{manifest_name}.yaml"
                )

        file = Path(file_location).is_file()
        if not file:
            e = f"{file_location} not found."
            raise RuntimeError(e)

        with open(file_location, "r") as checklist_yaml:
            try:
                test_config = yaml.safe_load(checklist_yaml)
            except Exception as e:
                LOG.l_exception(f"issue parsing yaml, please check: {e}")
        return test_config
