from datacoco_core.config import config
from datacoco_secretsmanager import SecretsManager


class ConfigWrapper:
    """

    Wrapper file for config management for hambot.
    """

    @staticmethod
    def sm_conf(project_name: str, team_name: str):
        """

        Simple config wrapper for using secrets manager.
        """
        c = SecretsManager().get_config(project_name, team_name)
        return c

    @staticmethod
    def parse(parser):

        parser.add_argument(
            "-m",
            "--manifest",
            help="Enter the manifest name that is in manifests folder. Do not include file extension.",
            default="sample",
        )
        parser.add_argument(
            "-t",
            "--db_log_table",
            help="Save execution results to target database table. Example: public.table_name",
        )

        parser.add_argument(
            "-p",
            "--parameters",
            help='Parameters to replace variables in queries. Example: "key1:val1,key2:val2"',
            required=False,
        )

        parser.add_argument(
            "-cfg",
            "--config",
            default="core",
            help="""
                whether to use secret_manager or
                datacoco_core to retrieve secrets
                """,
            choices=["secret_manager", "core"],
        )

        parser.add_argument(
            "-smp",
            "--secret_project_name",
            default="hambot",
            help="""
                secret manager project group
                """,
        )

        parser.add_argument(
            "-smt",
            "--secret_team",
            default="data",
            help="""
                secret manager team
                """,
        )
        return parser

    @staticmethod
    def process_config(args):
        if args.config == "secret_manager":
            conf = ConfigWrapper.sm_conf(
                project_name=args.secret_project_name,
                team_name=args.secret_team,
            )
        elif args.config == "core":
            conf = config()

        return conf
