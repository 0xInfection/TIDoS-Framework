#!/usr/bin/env python
import requests
from multiprocessing import Process, Queue, current_process

# buildmenu(target,dict,banner,art)

scraper_list = []

def scraper(target,process_queue, done_queue):
    print('HELLO SCRAPER', target[0].ip)
    print('PROCESS QUEUE', process_queue)
    print('DONE QUEUE', done_queue)
    scraper_list.append(target[0].ip)

    print('SCRAPER LIST', scraper_list)
