##########IMPORTS##########
from waybackpy import WaybackMachineCDXServerAPI
import datetime
import requests
from utils import functions
import toml


#########CONSTANTS##########
WILDCARD = "*"
UTF = 'unicode_escape'
DAYS = 90
delta = datetime.timedelta(DAYS)
t = datetime.datetime.now() - delta
start_timestamp = t.strftime('%Y%m%d%H%M%S')
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)


#########FUNCTIONS##########
def get_resources(url):
    """
    retrieving the last 90 days scanned resources of the url and search signatures
    :param url: the domain or specific url
    :return:
    """
    url = url + WILDCARD
    cdx = WaybackMachineCDXServerAPI(url, start_timestamp=start_timestamp)
    results = []

    counter = 0

    for item in cdx.snapshots():
        exceptions = conf['signatures']['exceptions']
        ext = item.archive_url.split(".")[-1]
        if ext not in exceptions:
            html = requests.get(item.archive_url).content
            res = functions.search_sign(html.decode(errors='ignore'), ext, item.archive_url)
            if res:
                results += res
            counter += 1
            print(str(counter) + " - " + url + " - " + ext)
    return results

