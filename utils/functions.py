##########IMPORTS##########
import csv
import datetime
import re
import requests
import toml

#########CONSTANTS##########
PATH = '/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/results/'
JS = ["js", "js/"]
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)


#########FUNCTIONS##########
def load_csv(file_path):
    """
    loading a csv file
    :param file_path: filepath string
    :return: list of list
    """
    with open(file_path, conf['constants']['read']) as f:
        csv_reader = csv.reader(f)
        return [i for i in csv_reader]


def write_result(results, domain):
    """
    write the results into results file
    :param results: list of strings
    :param domain: string
    :return: None
    """
    filename = PATH + str(datetime.datetime.now()) + conf['constants']['space'] + domain + conf['constants']['txt']
    to_write = ""
    for key in results.keys():
        to_write += key + " - " + str(results[key]) + conf['constants']['line'] + conf['constants']['line']

    with open(filename, conf['constants']['write']) as f:
        f.write(to_write)


def check_sign(sign, html, domain):
    """
    if sign in html return the sign, else None
    :param domain: the domain (string)
    :param html: the html (string)
    :param sign: the sign (sting)
    :return: sign (string)
    """
    res = re.compile(sign).findall(html)
    result_filtering = conf['signatures']['result_filtering']
    for r in res:
        if domain in r:
            return
    for r in result_filtering:
        for j in res:
            if r in j:
                return
    if res:
        print(res, sign, domain)
        return res


def import_blacklists():
    """
    importing around 650000 malicious ips and domains
    :return: list
    """
    blacks = conf['urls']['blacklist_url']
    blacklist = []
    for black in blacks:
        blacklist += requests.get(black).content.decode(conf['constants']['utf8']).split('\n')
    try:
        blacklist.remove('')
    except:
        pass
    return blacklist


def search_sign(html, file_type, url, domain, blacklist):
    """
    flicking throught the html file, reading the signs from the config file
    :param blacklist: large list
    :param domain: string
    :type url: the scanned url
    :param file_type: the type of the file
    :param html:
    :return: {sign:[urls],}
    """
    results = {}
    signs = conf['signatures']['signs']
    js_signs = conf['signatures']['js_signs']

    """
    for black in blacklist:
        if black in html:
            results[black] = [url]
            print(black, domain)
    """
    if file_type in JS:
        for js_sign in js_signs:
            res = check_sign(js_sign, html, domain)
            if res:
                for s in res:
                    if s in results.keys():
                        results[s].append(url)
                    else:
                        results[s] = [url]
    for sign in signs:
        res = check_sign(sign, html, domain)
        if res:
            for s in res:
                if s in results.keys():
                    results[s].append(url)
                else:
                    results[s] = [url]
    return results
