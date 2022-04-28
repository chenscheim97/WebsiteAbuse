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
PATH = '/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/results/'


#########FUNCTIONS##########
def get_resources(url):
    """
    retrieving the last 90 days scanned resources of the url and search signatures
    :param url: the domain or specific url
    :return:
    """
    url = url + conf['constants']['wild']
    cdx = WaybackMachineCDXServerAPI(url, start_timestamp=start_timestamp)
    snap = cdx.snapshots()
    mimes = conf['signatures']['mimetype']
    for item in snap:
        if item.mimetype not in mimes:
            continue
        # print(url[:-1] + "-" + str(counter))
        exceptions = conf['signatures']['exceptions']
        ext = item.archive_url.split(".")[-1]
        if ext not in exceptions:
            html = requests.get(item.archive_url).content
            functions.search_sign(html.decode(errors='ignore'), ext, item.archive_url, url[:-1], item.digest)
            # if res:
            #     functions.write_result(res, url[:-1])
            #     t = datetime.datetime.now().strftime('%Y%m')
            #     filename = PATH + str(t) + "_" + url[:-1].split('.')[0] + conf['constants']['html']
            #     if not exists(filename):
            #         logging.error(f'File: {filename} did not write correctly')


