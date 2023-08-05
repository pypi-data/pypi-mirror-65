import base64
from urllib import parse as parseurl
import requests
import time
from command_tool.utils.utils import logger, error_exit
import os


def check_scan(scan_id, project_id, apikey, baseurl):
    api = "v1/projects/%s/scans/%s/"
    endpoint = api % (project_id, scan_id)
    url = parseurl.urljoin(baseurl, endpoint)
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    result = requests.get(url=url, headers=headers)
    if result.status_code not in [200, 201]:
        return {"error": "failed to get scan"}
    return result.json().get("status"), result.json().get("scan_percentage")
    # async with session.get(url=url, headers=headers) as r:
    #     if r.status not in [200, 201]:
    #         return {"error": "failed to get scan"}
    #     scan_status = await r.json()
    #     return scan_status.get("status")


def get_report(scan_id, apikey, baseurl, report_format, output_path, project_id=None):
    # source code scan with bom detect
    if project_id is None:
        generate_report(scan_id, apikey, baseurl)
        return download_report(scan_id, apikey, baseurl, report_format, output_path)

    generate_report(scan_id, apikey, baseurl)
    download_report(scan_id, apikey, baseurl, report_format, output_path)

    # async with aiohttp.ClientSession() as session:
    #     is_download = False
    #     while not is_download:
    #         task = [check_scan(scan_id, project_id, apikey, baseurl, session)]
    #         for f in asyncio.as_completed(task, timeout=1800):
    #             status = await f
    #             if not status:
    #                 continue
    #
    #             if status == "finished":
    #
    #                 is_download = True


def generate_report(scan_id, apikey, baseurl):
    generate_component_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/library-versions/generate/" % scan_id
    )
    generate_vulnerability_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/issues/generate/" % scan_id
    )
    generate_licenses_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/licenseissues/generate/" % scan_id
    )
    generate_list = [
        generate_component_url,
        generate_vulnerability_url,
        generate_licenses_url,
    ]
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }

    for generate_url in generate_list:
        response = requests.post(generate_url, headers=headers)
        if response.status_code not in [200, 201]:
            error_exit("failed to generate report")
        logger.info(f"Starting generate report...")


def download_report(scan_id, apikey, baseurl, report_format, output_path=None):
    download_component_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/library-versions/export/" % scan_id
    )
    download_vulnerability_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/issues/export/" % scan_id
    )
    download_licenses_url = parseurl.urljoin(
        baseurl, "v1/scans/%s/licenseissues/export/" % scan_id
    )
    download_dict = {
        "component": download_component_url,
        "vulnerability": download_vulnerability_url,
        "licenses": download_licenses_url,
    }
    length = len(download_dict)

    header = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    query = {"report_format": report_format, "language": "english"}

    while length > 0:
        for key, url in download_dict.items():
            content = check_generate(url, header, query)

            if not content:
                time.sleep(5)
                continue

            length -= 1
            if report_format == "csv":
                content = base64.decodebytes(content)

            with open(
                os.path.join(
                    output_path,
                    f"scan-{scan_id}-{key}.csv"
                    if report_format == "csv"
                    else f"scan-{scan_id}-{key}.pdf",
                ),
                "wb",
            ) as f:
                f.write(content)
    logger.info(f"Successful download scan report!")


def check_generate(url, header, query):
    response = requests.get(url, headers=header, params=query)
    if response.status_code not in [200, 201]:
        return None

    content = response.content
    content = base64.decodebytes(content)
    return content
