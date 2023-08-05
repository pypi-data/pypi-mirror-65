"""
this will be the main entry point to the program, will probably end up being a flask web service, with a basic UI
"""

import os

# from pprint import pprint
from datacoco_core import Logger
from datacoco_cloud.athena_interaction import AthenaInteraction

LOG = Logger()


class SqlComp(object):
    """

    """

    def __init__(self, test_conf, paramDict=None):
        """

        :param test_conf:
        :return:
        """
        print(f"=====>>>>> test_conf: {test_conf}")
        if paramDict is not None:
            print(f"=====>>>>> params: {paramDict}")

        self.test_conf = test_conf
        self.params = paramDict

    def setup(self, config: dict = None):
        self.config = config
        return self

    @staticmethod
    def get_script(script, params=None):
        """

        :param script:
        :return:
        """

        def expand_params(sql):
            """
            substitutes params in sql stagement
            :param sql:
            :param params:
            :return: sql, expanded with params
            """
            if params is None:
                return sql

            for p in params.keys():
                var = "$[?" + p + "]"
                val = str(params[p])
                sql = sql.replace(var, val)
            return sql

        if script[-4:] == ".sql":
            with open(script, "r") as myfile:
                script_data = myfile.read()
        else:
            script_data = script

        script_data = expand_params(script_data)
        return script_data

    def run(self):
        """
        :return: tuple
        """
        label = self.test_conf["label"]
        conn_a = self.test_conf["conn_a"]
        conn_b = self.test_conf["conn_b"]

        if self.params is None:
            script_a = self.get_script(self.test_conf["script_a"]).split(";")
            script_b = self.get_script(self.test_conf["script_b"]).split(";")
        else:
            script_a = self.get_script(
                self.test_conf["script_a"], self.params
            ).split(";")
            script_b = self.get_script(
                self.test_conf["script_b"], self.params
            ).split(";")

        warning_threshold = self.test_conf.get("warning_threshold", 1)
        failure_threshold = self.test_conf.get("failure_threshold", 1)
        percent_diff = self.test_conf.get("pct_diff", False)
        heartbeat = self.test_conf.get("heartbeat", False)
        ath_conn = AthenaInteraction(
            self.config["general"]["aws_access_key"],
            self.config["general"]["aws_secret_key"],
            self.config["general"]["region"],
        )

        LOG.l(
            "\n---------------------------------------------------------------------\n"
            + label
            + "\n---------------------------------------------------------------------\n"
        )
        print(f"conn_a: {conn_a}")
        print(f"conn_b: {conn_b}")

        LOG.l("\nscript_a: \n" + ";".join(script_a) + "\n")
        res_a = []
        for query in script_a:
            queryid, result = ath_conn.exec_query(query, conn_a)
            if len(result["ResultSet"]["Rows"]) > 0:
                res_a_fmt = ath_conn.format_results(result, "|")
                res_a = res_a_fmt.split("\n")

        LOG.l("script_b: \n" + ";".join(script_b) + "\n")
        res_b = []
        for query in script_b:
            queryid, result = ath_conn.exec_query(query, conn_b)
            if len(result["ResultSet"]["Rows"]) > 0:
                res_b_fmt = ath_conn.format_results(result, "|")
                res_b = res_b_fmt.split("\n")

        diff = list(set(res_a).symmetric_difference(set(res_b)))

        # Percentage difference is True
        if percent_diff:
            diff_pct = 1 - (len(res_b) / len(res_a))
            if diff_pct >= failure_threshold:
                status = "failure"
            elif diff_pct >= warning_threshold:
                status = "warning"
            else:
                diff = None
                status = "success"

        # Percentage difference is False
        else:
            diff_cnt = len(diff)
            if diff_cnt >= failure_threshold:
                status = "failure"
            elif diff_cnt >= warning_threshold:
                status = "warning"
            else:
                diff = None
                status = "success"

        detail = {
            "status": status,
            "test": label,
            "result_a": res_a,
            "result_b": res_b,
            "diff": diff,
            "test_conf": self.test_conf,
            "parameters": self.params,
        }

        return status, detail
