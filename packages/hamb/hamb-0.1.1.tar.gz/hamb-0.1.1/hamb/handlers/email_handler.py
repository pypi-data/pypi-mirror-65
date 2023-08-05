"""
email handler
"""

import os
import json
import pandas as pd
from datetime import datetime
from datacoco_email_tools import Email


class Handler(object):
    def __init__(self, config):
        self.environment = config["hambot"]["environment"]
        self.aws_conf = config["aws"]
        self.aws_key = self.aws_conf["aws_key"]
        self.aws_id = self.aws_conf["aws_id"]
        self.ses_def_sender = self.aws_conf["ses_def_sender"]
        self.ses_region = self.aws_conf["ses_region"]

        self.os = None

    def setup(self):
        self.os = os
        return self

    def run(self, result, conf):
        """
        :param result:
        :param conf:
        :return:
        """
        recipients = conf.split(" ")

        level = result["summary"]["status"]
        manifest = result["summary"]["manifest"]
        subject = (
            str(self.environment).upper()
            + str(" Hambot %s: %s" % (level, manifest)).title()
        )

        with_attachment = os.path.exists("diagnostic_query_results.csv")

        if level == "success" or not with_attachment:
            json_msg = json.dumps(result, indent=4, default=json_serializer)
            if self.environment != "dev":
                Email.send_mail(
                    aws_access_key=self.aws_id,
                    aws_secret_key=self.aws_key,
                    aws_sender=self.ses_def_sender,
                    aws_region=self.ses_region,
                    to_addr=recipients,
                    subject=subject,
                    text_msg=json_msg,
                )

        else:
            json_msg = (
                json.dumps(result, indent=4, default=json_serializer)
                .replace(" ", "&nbsp;")
                .replace("\n", "<br>")
            )
            if self.environment != "dev":
                Email.send_email_with_attachment(
                    aws_access_key=self.aws_id,
                    aws_secret_key=self.aws_key,
                    aws_sender=self.ses_def_sender,
                    aws_region=self.ses_region,
                    to_addr=recipients,
                    subject=subject,
                    body_msg=json_msg,
                    filename="diagnostic_query_results.csv",
                )
            self.os.remove("diagnostic_query_results.csv")


def render_html(result):
    """
        builds html message
        :return:
        """
    html_table = """
<table border="1" cellpadding="0" cellspacing="0" bordercolor=#BLACK>
"""
    html_header = """<tr> <td> Jobs Status </td> </tr>"""
    # Make <tr>-pairs, then join them.
    # html += "\n".join(
    # map(
    #     lambda x: """
    #     <td style="width: 175px;">
    #     """ + str(result) + "</td>", 1)
    # )
    html_result = f"<tr> <td> {result} </td> </tr></table> <br><br>"
    html = html_table + html_header + html_result
    return html


def json_serializer(data):
    """
    JSON serializer for objects not serializable by default json code"
    :param obj:
    :return:
    """

    if isinstance(data, pd.DataFrame):
        table = data.to_json(orient="split")
        table = table.replace('"', "")
        x = table.split("data", 1)
        return x[1]
    elif isinstance(data, datetime):
        serial = data.isoformat()
        return serial
    raise TypeError("Type not serializable")
