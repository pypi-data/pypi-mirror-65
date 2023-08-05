import requests
from urllib import parse as parseurl
from command_tool.utils.utils import error_exit, logger


def get_scan_library_versions_overview(scan_id, apikey, baseurl):
    api = f'/v1/scans/{scan_id}/library-versions/overview/'
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan components information")
    
    logger.debug(f"[get_scan_library_versions_overview]\n{result.json()}")
    return result.json()['library_count'], result.json()['vulnerable_libraries_count']


def get_scan_issues_overview(scan_id, apikey, baseurl):
    api = f'/v1/scans/{scan_id}/issues/?limit=99999&page=1'
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan vulnerability information")

    return len(result.json()['results'])


def get_scan_license_overview(scan_id, apikey, baseurl):
    api = f'/v1/scans/{scan_id}/licenseissues/?limit=99999&page=1'
    headers = {
        "Authorization": "Token " + apikey,
        "Content-Type": "application/json; charset=utf-8",
    }
    url = parseurl.urljoin(baseurl, api)
    result = requests.get(url=url, headers=headers)

    if result.status_code != 200:
        error_exit("Fail to get scan license issue information")

    return len(result.json()['results'])


def get_scan_summary(scan_id, apikey, baseurl):
    (
        scan_components_count,
        scan_vul_components_count,
    ) = get_scan_library_versions_overview(scan_id, apikey, baseurl)
    scan_vulnerability_count = get_scan_issues_overview(scan_id, apikey, baseurl)
    scan_licenseissue_count = get_scan_license_overview(scan_id, apikey, baseurl)

    print(
        f"scan_components_count : {scan_components_count}, scan_vul_components_count : {scan_vul_components_count}\nscan_vulnerability_count : {scan_vulnerability_count}, scan_licenseissue_count : {scan_licenseissue_count}"
    )