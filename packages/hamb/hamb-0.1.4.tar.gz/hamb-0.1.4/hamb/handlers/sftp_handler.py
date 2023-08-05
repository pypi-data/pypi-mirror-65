"""
drops watch file in sftp folder per [hamb] config section.
"""
from time import sleep
from datacoco_core import Logger
from datacoco_ftp_tools import FTPInteraction

LOG = Logger()


class Handler(object):
    def __init__(self, config):
        self.host = config["hamb_sftp"]["site"]
        self.user = config["hamb_sftp"]["user"]
        self.password = config["hamb_sftp"]["password"]
        self.environment = config["hambot"]["environment"]
        self.path = config["hamb_sftp"]["path"]
        self.SFTP = None

    def setup(self):
        self.SFTP = FTPInteraction(
            protocol="sftp",
            host=self.host,
            user=self.user,
            password=self.password,
        )

        return self

    def run(self, result, conf):
        level = result["summary"]["status"]

        if level == "failure":
            LOG.l("exiting")
            return

        file_name = str(self.environment).lower() + "_" + conf

        self.SFTP.conn()
        self.SFTP.sftp_conn.chdir(self.path)

        LOG.l("listing files:")
        for f in self.SFTP.sftp_conn.listdir():
            LOG.l(f)
            if f == file_name:
                self.SFTP.sftp_conn.remove(f)

        with open(file_name, "wb") as f:
            if self.environment != "dev":
                f.write("yippee")

        sleep(10)

        LOG.l("uploading to SFTP")
        self.SFTP.write_file(file_name, self.path)
        LOG.l("SFTP upload complete")

        self.SFTP.quit()
