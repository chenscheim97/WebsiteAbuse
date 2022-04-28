##########IMPORTS##########
from utils import wayback, functions
import time
import toml
from multiprocessing import Pool
import random
import logging


#########CONSTANTS##########
COMPANY = ""
CSV = 'datasets/companies.csv'
DOMAIN_LOCATION = 1
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)
LIMIT = conf['constants']['company_limit']
logging.basicConfig(filename='datasets/example.log', level=logging.DEBUG)


if __name__ == '__main__':
    domains = [i[DOMAIN_LOCATION] for i in functions.load_csv(CSV)[conf['constants']['one']:LIMIT]]
    random.shuffle(domains)  # shuffling the list
    for i in range(conf['constants']['zero'], len(domains), conf['constants']['multiprocess']):
        start = time.perf_counter()
        urls = domains[i:i+conf['constants']['multiprocess']]
        p = Pool(conf['constants']['multiprocess'])
        for url in urls:
            logging.info(f'Looking for {url}')
            p.apply_async(wayback.get_resources, args=(url,))
            logging.info(f'The url {url} has scanned')
        p.close()
        p.join()

        end = time.perf_counter()
        logging.info(f'Run time is: {(end - start) / 60} minuets')
        print((end - start) / 60, 'minutes')
