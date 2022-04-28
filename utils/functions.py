##########IMPORTS##########
import csv
import datetime
import re
import toml
from os.path import exists
import virustotal_python
from pprint import pprint
import logging


#########CONSTANTS##########
PATH = '/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/results/'
JS = ["js", "js/"]
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)
LINE = conf['constants']['line']
logging.basicConfig(filename='datasets/example.log', level=logging.DEBUG)


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
    t = datetime.datetime.now().strftime('%Y%m')
    filename = PATH + str(t) + conf['constants']['under'] + domain.split('.')[0] + conf['constants']['html']
    keys = list(results.keys())
    to_write = f"<!-- {conf['constants']['under'].join(keys + [results[keys[-1]][0]] + [domain])} --> \n"\
               + results[keys[-1]][-1]
    if not exists(filename):
        with open(filename, conf['constants']['write']) as f_name:
            f_name.write(to_write)


def search_vt(digest):
    """
    using VT API to search files in VT
    :param digest: The ID (either SHA-256, SHA-1 or MD5 hash) identifying the file
    :return:
    """
    print(digest)
    with virustotal_python.Virustotal(conf['constants']['vt_api']) as vtotal:
        try:
            resp = vtotal.request(f"files/{digest}")
            pprint(resp.data)
            if resp.data:
                return resp.data
        except Exception as e:
            logging.error(f'Virus Total Error - {e}')


def check_sign(sign, html, domain, digest):
    """
    if sign in html return the sign, else None
    :param domain: the domain (string)
    :param html: the html (string)
    :param sign: the sign (sting)
    :param digest: The ID (either SHA-256, SHA-1 or MD5 hash) identifying the file
    :return: sign (string)
    """
    res = re.compile(sign).findall(html)
    result_filtering = conf['signatures']['result_filtering']
    for r in res:
        if domain in r:
            return [], []
    for r in result_filtering:
        for j in res:
            if r in j:
                return [], []
    if res:
        print(res, sign, domain)
        vt_res = search_vt(digest)
        return res, vt_res
    return [], []


def search_sign(html, file_type, url, domain, digest):
    """
    flicking throught the html file, reading the signs from the config file
    :param digest: the SHA-1 of the file
    :param domain: string
    :type url: the scanned url
    :param file_type: the type of the file
    :param html:
    :return: {sign:[urls],}
    """
    results = {}
    signs = conf['signatures']['signs']

    if file_type in JS:
        signs = conf['signatures']['js_signs']
    for sign in signs:
        res, vt_res = check_sign(sign, html, domain, digest)
        if res:
            results[digest] = vt_res
            for s in res:
                if s in results.keys():
                    results[s].append([url, html])
                else:
                    results[s] = [url, html]
    if results:
        write_result(results, domain)
        t = datetime.datetime.now().strftime('%Y%m')
        filename = PATH + str(t) + "_" + url[:-1].split('.')[0] + conf['constants']['html']
        if not exists(filename):
            logging.error(f'File: {filename} did not write correctly')
