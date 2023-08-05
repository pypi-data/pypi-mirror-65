"""
this will be the main entry point to the program
"""

import os
import csv

from datacoco_core import Logger
from datacoco_db.rdb_tools import DBInteraction

LOG = Logger()


class SqlCompare(object):
    """

    """

    def __init__(self, test_conf):
        """

        :param test_conf:
        :return:
        """
        print(f"=====>>>>> test_conf: {test_conf}")
        self.test_conf = test_conf
        self.conn_a = self.test_conf["conn_a"]
        self.conn_b = self.test_conf["conn_b"]
        print(f"conn_a: {self.conn_a}")
        print(f"conn_b: {self.conn_b}")
        self.aws_access_key = None
        self.aws_secret_key = None

    def setup(self, config: dict):
        self.conn_a = DBInteraction(
            dbtype=config[self.conn_a]["type"],
            dbname=config[self.conn_a]["db_name"],
            host=config[self.conn_a]["host"],
            user=config[self.conn_a]["user"],
            password=config[self.conn_a]["password"],
            port=config[self.conn_a]["port"],
        )
        self.conn_b = DBInteraction(
            dbtype=config[self.conn_b]["type"],
            dbname=config[self.conn_b]["db_name"],
            host=config[self.conn_b]["host"],
            user=config[self.conn_b]["user"],
            password=config[self.conn_b]["password"],
            port=config[self.conn_b]["port"],
        )

        return self

    def get_script(self, script):
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

            params = {
                "aws_access_key": self.aws_access_key,
                "aws_secret_key": self.aws_secret_key,
            }

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

        :return:
        """

        def convert_types(num):
            if not num:
                num = 0
            if num % 1 == 0:
                return int(num)
            else:
                return float(num)

        label = self.test_conf["label"]
        script_a = self.get_script(self.test_conf["script_a"])
        script_b = self.get_script(self.test_conf["script_b"])
        warning_threshold = self.test_conf.get("warning_threshold", 1)
        failure_threshold = self.test_conf.get("failure_threshold", 1)
        percent_diff = self.test_conf.get("pct_diff", False)
        heartbeat = self.test_conf.get("heartbeat", False)
        d_query_a = self.test_conf.get("diagnostic_query_a", None)
        d_query_b = self.test_conf.get("diagnostic_query_b", None)

        if d_query_a:
            diagnostic_query_a = self.get_script(d_query_a)
        if d_query_b:
            diagnostic_query_b = self.get_script(d_query_b)

        LOG.l(
            "\n-----------------------\
            --------------------------\
            --------------------\n"
            + label
            + "\n---------------------\
            --------------------------\
            --------------------\n"
        )

        LOG.l("script_a: \n" + script_a + "\n")
        LOG.l("script_b: \n" + script_b + "\n")

        result_a = convert_types(self.conn_a.fetch_sql_one(script_a)[0])
        result_b = convert_types(self.conn_b.fetch_sql_one(script_b)[0])

        if percent_diff:
            LOG.l("comparison mode: percent diff")
            denominator = result_a if result_a and result_a != 0 else 1
            diff = abs(result_a - result_b) / float(denominator)
        else:
            LOG.l("comparison mode: absolute")
            diff = abs(result_a - result_b)

        status = ""
        if heartbeat:
            LOG.l("heartbeat mode")
            if diff <= failure_threshold:
                status = "failure"
            elif diff <= warning_threshold:
                status = "warning"
            else:
                status = "success"
        else:
            if diff >= failure_threshold:
                status = "failure"
            elif diff >= warning_threshold:
                status = "warning"
            else:
                status = "success"

        if status != "success" and d_query_a or d_query_b:
            if os.path.isfile("diagnostic_query_results.csv"):
                q_results = open("diagnostic_query_results.csv", "a")
            else:
                q_results = open("diagnostic_query_results.csv", "w")

            res_csv = csv.writer(q_results)
            res_csv.writerow([label])

            if d_query_a:
                res_a = self.conn_a.con.execute(diagnostic_query_a)
                res_csv.writerow(res_a.keys())
                res_csv.writerows(res_a)
            if d_query_b:
                res_b = self.conn_b.con.execute(diagnostic_query_b)
                res_csv.writerow(res_b.keys())
                res_csv.writerows(res_b)

            res_csv.writerow("\n")
            q_results.close()

        detail = {
            "status": status,
            "test": label,
            "result_a": result_a,
            "result_b": result_b,
            "diff": diff,
            "test_conf": self.test_conf,
        }

        return status, detail
