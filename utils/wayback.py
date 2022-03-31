##########IMPORTS##########
from waybackpy import WaybackMachineCDXServerAPI
import datetime
import requests

WILDCARD = "*"
DAYS = 90
delta = datetime.timedelta(DAYS)
t = datetime.datetime.now() - delta
start_timestamp = t.strftime('%Y%m%d%H%M%S')


def get_resources(url):
    """
    retriving the last 90 days scanned resources of the url
    :param url: the domain or specific url
    :return:
    """
    url = url + WILDCARD
    cdx = WaybackMachineCDXServerAPI(url, start_timestamp=start_timestamp)

    counter = 0
    for item in cdx.snapshots():
        # print(item.archive_url)
        # html = requests.get(item.archive_url).content
        counter += 1

    print(counter)
