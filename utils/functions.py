import csv
import datetime
import re
import toml


EXTENSION = '.txt'
PATH = '/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/results/'


def load_csv(file_path):
    """
    loading a csv file
    :param file_path: filepath string
    :return: list of list
    """
    with open(file_path, 'r') as f:
        csv_reader = csv.reader(f)
        return [i for i in csv_reader]


def write_result(results, domain):
    """
    write the results into results file
    :param results: list of strings
    :param domain: string
    :return: None
    """
    filename = PATH + str(datetime.datetime.now()) + domain.split('.')[-2] + EXTENSION
    with open(filename, 'w') as f:
        print(type(results))
        print(results)
        f.write('\r\n'.join(results))


def search_sign(html):
    """
    flicking throught the html file, reading the signs from the config file
    :param html:
    :return:
    """
    results = []
    with open('datasets/config.toml', 'r') as f:
        conf = toml.load(f)
        signs = conf['signatures']['signs']
        results += re.compile('|'.join(signs)).findall(html)
    return results