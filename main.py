##########IMPORTS##########
from utils import wayback, functions
import time
from multiprocessing import Pool


#########CONSTANTS##########
COMPANY = ""
CSV = 'datasets/bitsight-technologies-portfolio-all-companies-2022-03-17-2.csv'
MP = 10


if __name__ == '__main__':
    start = time.perf_counter()
    domains = [i[3] for i in functions.load_csv(CSV)[1:50]]
    for i in range(0, len(domains), 3):
        url = domains[i:i+MP]
        print(url)

        with Pool(MP) as p:
            results = p.map(wayback.get_resources, url)
        # results = wayback.get_resources(url)

        if results:
            functions.write_result(results)
        break

    end = time.perf_counter()

    print(end - start)