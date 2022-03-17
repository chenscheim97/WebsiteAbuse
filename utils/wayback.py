##########IMPORTS##########
from waybackpy import WaybackMachineCDXServerAPI
import datetime
import requests

url = "ynet.co.il*"

delta = datetime.timedelta(90)
t = datetime.datetime.now() - delta
start_timestamp = t.strftime('%Y%m%d%H%M%S')

cdx = WaybackMachineCDXServerAPI(url, start_timestamp=start_timestamp)


counter = 10
for item in cdx.snapshots():
    # print(item.archive_url)
    html = requests.get(item.archive_url).content

