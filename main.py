from utils import wayback, functions
import time

COMPANY = ""
CSV = 'datasets/bitsight-technologies-portfolio-all-companies-2022-03-17-2.csv'


if __name__ == '__main__':
    start = time.perf_counter()
    domains = [i[3] for i in functions.load_csv(CSV)[1:50]]
    for url in domains:
        print(url)
        wayback.get_resources(url)

    end = time.perf_counter()
    print(end - start)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
