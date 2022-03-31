##########IMPORTS##########
import csv
import datetime
import re
import toml

#########CONSTANTS##########
FILE_EXTENSION = '.txt'
PATH = '/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/results/'
JS = ["js", "js/"]


#########FUNCTIONS##########
def load_csv(file_path):
    """
    loading a csv file
    :param file_path: filepath string
    :return: list of list
    """
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        return [i for i in csv_reader]


def write_result(results):
    """
    write the results into results file
    :param results: list of strings
    :param domain: string
    :return: None
    """
    filename = PATH + str(datetime.datetime.now()) + FILE_EXTENSION
    with open(filename, 'w') as f:
        print(type(results))
        print(results)
        f.write('\r\n'.join([str(i) for i in results]))


def search_sign(html, file_type, url):
    """
    flicking throught the html file, reading the signs from the config file
    :param file_type: the type of the file
    :param html:
    :return:
    """
    results = {}
    with open('datasets/config.toml', 'r') as f:
        conf = toml.load(f)
        signs = conf['signatures']['signs']
        results[url] = re.compile('|'.join(signs)).findall(html)
        if file_type in JS:
            js_signs = conf['signatures']['js_signs']
            results[url] += re.compile('|'.join(js_signs)).findall(html)
    return results


