import re
import toml


def search_sign(html):
    """
    flicking throught the html file, reading the signs from the config file
    :param html:
    :return:
    """
    results = []
    with open('/Users/chenscheim/PycharmProjects/WebsiteAbuse/datasets/config.toml', 'r') as f:
        conf = toml.load(f)
        signs = conf['signatures']['signs']
        results.append(re.compile('|'.join(signs)).findall(html))
    return results



