##########IMPORTS##########
from waybackpy import WaybackMachineCDXServerAPI
import datetime
import requests
from utils import functions
import toml


#########CONSTANTS##########
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)
UTF = 'unicode_escape'
DAYS = conf['limits']['days_ago']
delta = datetime.timedelta(DAYS)
t = datetime.datetime.now() - delta
start_timestamp = t.strftime('%Y%m%d%H%M%S')


#########FUNCTIONS##########
def get_resources(url, blacklist):
    """
    retrieving the last 90 days scanned resources of the url and search signatures
    :param blacklist: large list
    :param url: the domain or specific url
    :return:
    """
    # counter = 1
    url = url + conf['constants']['wild']
    cdx = WaybackMachineCDXServerAPI(url, start_timestamp=start_timestamp)
    snap = cdx.snapshots()
    for item in snap:
        # print(url[:-1] + "-" + str(counter))
        exceptions = conf['signatures']['exceptions']
        ext = item.archive_url.split(".")[-1]
        if ext not in exceptions:
            html = requests.get(item.archive_url).content
            res = functions.search_sign(html.decode(errors='ignore'), ext, item.archive_url, url[:-1], blacklist)
            if res:
                functions.write_result(res, url[:-1])

        # counter += 1

