import sys
import getopt
import logging
from command_tool.utils.login import login
from command_tool.utils.utils import error_exit, set_config

FORMAT = "%(asctime)s|%(levelname)s|%(message)s"
logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO, format=FORMAT)


HELP_CONTENT = """
Login and save credentials
\t> scantist_auth -b $baseurl -e $email -p $password
Set up base url and apikey:
\t> scantist_auth -b $base_url -a apikey
"""


def main():
    argv = sys.argv[1:]
    opts = []
    args = []
    email = ""
    password = ""
    base_url = ""
    api_key = ""
    
    try:
        opts, args = getopt.getopt(
            argv,
            "hle:p:b:a:",
            [
                "email=",
                "password=",
                "base_url=",
                "api_key=",
            ],
        )
    except Exception as e:
        error_exit(e)

    if len(args) == 0 and len(opts) == 0:
        logger.info(HELP_CONTENT)
        exit(0)

    for opt, arg in opts:
        if opt == "-h":
            logger.info(HELP_CONTENT)
            sys.exit()
        elif opt in ("-e", "--email"):
            email = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-b", "--base_url"):
            base_url = arg
        elif opt in ("-a", "--api_key"):
            api_key = arg

    if api_key:
        set_config("SCANTIST", "base_url", base_url)
        set_config("SCANTIST", "api_key", api_key)
        exit(0)

    r = login(email, password, "", base_url)
    set_config("SCANTIST", "base_url", base_url)
    logger.info(f"[LOGIN]==>{r}")

#
# if __name__ == "__main__":
#     main(sys.argv[1:])
