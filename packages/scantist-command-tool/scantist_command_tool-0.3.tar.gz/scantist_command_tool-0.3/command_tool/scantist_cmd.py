#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import os
import time
from datetime import datetime
from command_tool.utils.utils import logger, error_exit, config, ScanType, zip_folder
from command_tool.utils.user import show_user
from command_tool.utils.login import login, create_scantist_token
from command_tool.utils.project import show_projects, set_proj, get_proj_id
from command_tool.utils.scan import (
    scan_latest_version,
    scan_sourcecode,
    scan_upload_proj,
    get_scan_id,
)
from command_tool.utils.report import get_report, check_scan
from command_tool.utils.scan_result import get_scan_summary

HELP_CONTENT = """
## Binary Scan
- scantist_cmd -t binary -f $local_file_path 

- optional parameter: 
        
        -r [csv|pdf]: download scan report
        
        -v          : set the version of the project
        
        -p          : set the project name. if this parameter is null, will use file name as project name
        
        -j          : project id.
        
        -h          : report output path. Default path is current working directory.
        
file + version -> create new project, name by file.【if duplicate name project exist, will update the project】

file + version + project_name -> create new project, name by the project_name.

local_binary_file + version + project_id -> create new version of existing project.

project_id -> scan existing project.

## Source code scan
- scantist_cmd -t source_code -f $local_file_path 

- optional parameter :

        -r [csv|pdf]: download scan report
        
        -h          : report output path. Default path is current working directory.
        
## List user projects
- scantist_cmd -l


## Download scan result
Generate and download the most recent scan report if no $project_id given
- scantist_cmd -r ["csv"|"pdf"]

- optional parameter:

        -j  : project id.
"""


def main():
    argv = sys.argv[1:]
    scan_type = ""
    local_file = ""
    version = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    opts = []
    list_projects = False
    report_format = ""
    args = []
    # zip_paths = ""
    # source_code_zip = False
    project_name = ""
    project_id = 0
    report_path = os.path.join(os.getcwd(), "report")

    try:
        opts, args = getopt.getopt(
            argv,
            "hult:f:v:r:j:z:p:h",
            [
                "scan_type=",
                "file_path=",
                "version=",
                "report_format=",
                "project_id=",
                "zip_paths=",
                "project_name=",
                "report_path=",
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
        elif opt in ("-t", "--scan_type"):
            scan_type = arg
        elif opt in ("-f", "--file"):
            local_file = arg
        elif opt in ("-v", "--version"):
            version = arg
        elif opt in ("-l", "--list_projects"):
            list_projects = True
        elif opt in ("-r", "--report"):
            if arg != "csv" and arg != "pdf":
                error_exit("Scan report only accept csv or pdf format.")
            report_format = arg
        elif opt in ("-h", "--report_path"):
            report_path = arg
        elif opt in ("-j", "--project_id"):
            project_id = arg
        # elif opt in ("-z", "--zip_paths"):
        #     zip_paths = arg
        # elif opt in ("-u", "--upload_source"):
        #     source_code_zip = True
        elif opt in ("-p", "--project_name"):
            project_name = arg

    baseurl = config.get("SCANTIST", "BASE_URL")
    email = config.get("SCANTIST", "EMAIL")
    password = config.get("SCANTIST", "PASSWORD")
    oauth_token = config.get("SCANTIST", "OAUTH_TOKEN")
    scantist_token = config.get("SCANTIST", "SCANTIST_TOKEN")
    apikey = config.get("SCANTIST", "API_KEY")

    if not apikey or not baseurl:
        error_exit("Please using 'scantist_auth' command set up account first.")

    user_info = show_user(apikey, baseurl)
    logger.info(f"Hello! {user_info['user_name']}")

    # get apikey and scantist token
    if not scantist_token:
        logger.info("Generating scantist_token...")
        default_org_id = user_info["default_org"]
        scantist_token = create_scantist_token(apikey, baseurl, default_org_id)

    if list_projects:
        show_projects(apikey, baseurl)
        exit(0)

    scan_id = 0

    if scan_type:
        if scan_type == ScanType.BINARY:
            # Binary Scan
            if local_file:
                # create new scan and upload local file
                if os.path.isfile(local_file):
                    binary_file = local_file
                elif os.path.isdir(local_file):
                    binary_file = zip_folder(local_file)
                else:
                    error_exit("Please provide a valid file path")

                logger.info("Setting project info...")
                (project_id, project_name) = set_proj(
                    apikey, baseurl, project_id, project_name, binary_file
                )
                logger.debug(f"project id: {project_id}, project name: {project_name}")
                (scan_id, project_id) = scan_upload_proj(
                    binary_file, apikey, baseurl, version, ScanType.BINARY, project_id
                )
                logger.debug(f"project id: {project_id}, scan_id: {scan_id}")
            else:
                # scan the latest version if only provide project id
                if project_id:
                    logger.info(
                        "Only project id provided, will scan the latest version of the project."
                    )
                    (scan_id, project_id) = scan_latest_version(
                        apikey, baseurl, ScanType.BINARY, project_id
                    )
                    logger.debug(f"project id: {project_id}, scan_id: {scan_id}")
                else:
                    error_exit("Please provide either project id or file path.")
        elif scan_type == ScanType.SOURCE_CODE:
            # Source code Scan
            if not os.path.isdir(local_file):
                error_exit("for source code scan, please specify a valid folder path")

            scan_id = scan_sourcecode(local_file, scantist_token, baseurl)
            project_id = get_proj_id(apikey, baseurl, scan_id)

        status = ""
        percentage = 0
        while status != "finished" and status != "failed":
            status, scan_percentage = check_scan(scan_id, project_id, apikey, baseurl)
            if scan_percentage and scan_percentage != percentage:
                percentage = scan_percentage
                logger.info("scan percentage: " + str(percentage) + "%")
            time.sleep(5)
        logger.info(f"Scan {scan_id} completed!")

    # project_id does not exist in source code scan
    # scan_sourcecode finish means scan finish, no need to check scan status, thus no need project id.
    # loop = asyncio.get_event_loop()
    if report_format:
        
        output_folder = os.path.join(
            report_path,
            os.path.splitext(os.path.basename(local_file))[0]
            if os.path.isfile(local_file)
            else os.path.basename(local_file) + "-report",
        )
        logger.info(f"report output folder: {output_folder}")

        if not os.path.exists(report_path):
            os.mkdir(report_path)

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        if scan_type:
            # loop.run_until_complete(
            #     check_report(
            #         scan_id,
            #         apikey,
            #         baseurl,
            #         report_format,
            #         output_folder,
            #         project_id if project_id else None,
            #     )
            # )
            get_report(
                scan_id,
                apikey,
                baseurl,
                report_format,
                output_folder,
                project_id if project_id else None,
            )
        else:
            # download report for the latest scan
            logger.info("Getting the most recent scan id...")
            scan_id = get_scan_id(apikey, baseurl, project_id)
            # loop.run_until_complete(
            #     get_report(scan_id, apikey, baseurl, report_format, output_folder)
            # )
            logger.info(f"Generalize report for scan {scan_id}")
            get_report(scan_id, apikey, baseurl, report_format, output_folder)

    get_scan_summary(scan_id, apikey, baseurl)
