##########IMPORTS##########
from utils import wayback, functions
import time
import toml
from multiprocessing import Pool


#########CONSTANTS##########
COMPANY = ""
CSV = 'datasets/bitsight-technologies-portfolio-all-companies-2022-03-17-2.csv'
DOMAIN_LOCATION = 3
LIMIT = 50
with open('datasets/config.toml', 'r') as f:
    conf = toml.load(f)


if __name__ == '__main__':
    start = time.perf_counter()
    domains = [i[DOMAIN_LOCATION] for i in functions.load_csv(CSV)[conf['constants']['one']:LIMIT]]
    blacklist = functions.import_blacklists()
    for i in range(conf['constants']['zero'], len(domains), conf['constants']['multiprocess']):
        urls = domains[i:i+conf['constants']['multiprocess']]
        p = Pool(conf['constants']['multiprocess'])
        for url in urls:
            p.apply_async(wayback.get_resources, args=(url, blacklist))
        p.close()
        p.join()

    end = time.perf_counter()
    print(end - start)
