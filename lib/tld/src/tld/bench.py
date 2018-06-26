from timeit import default_timer as timer
from faker import Faker
from tld import get_tld


fake = Faker()
fake.seed(1234)

URLS_COUNT = 1000
URLS = [fake.url() for _ in range(URLS_COUNT)]
TIMES = 10000

start = timer()
for _ in range(TIMES):
    for url in URLS:
        tld = get_tld(url)

print('get_tld:', timer() - start)
