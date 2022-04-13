##########IMPORTS##########
from utils import wayback, functions
import time
import toml
from multiprocessing import Pool
import random


#########CONSTANTS##########
COMPANY = ""
CSV = 'datasets/bitsight-technologies-portfolio-all-companies-2022-03-17-2.csv'
DOMAIN_LOCATION = 3
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)
LIMIT = conf['constants']['company_limit']


if __name__ == '__main__':
    start = time.perf_counter()
    domains = [i[DOMAIN_LOCATION] for i in functions.load_csv(CSV)[conf['constants']['one']:LIMIT]]
    random.shuffle(domains)  # shuffling the list
    blacklist = functions.import_blacklists()
    counter = 1
    for i in range(conf['constants']['zero'], len(domains), conf['constants']['multiprocess']):
        urls = domains[i:i+conf['constants']['multiprocess']]
        p = Pool(conf['constants']['multiprocess'])
        for url in urls:
            p.apply_async(wayback.get_resources, args=(url, blacklist))
        p.close()
        p.join()
        counter += conf['constants']['multiprocess']

    end = time.perf_counter()
    print(end - start)
