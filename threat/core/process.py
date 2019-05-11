#!/usr/bin/env python
from multiprocessing import Lock, Process, Queue, current_process
import time
import queue # imported for using queue.Empty exception
from threat import processes, tasks_that_are_done, tasks_to_accomplish
from .colors import color

NUM_WORKERS = 4#multiprocessing.cpu_count()

def do_job(func,tgt):#,tasks_to_accomplish, tasks_that_are_done):
    while True:
        try:
            '''
                try to get task from the queue. get_nowait() function will
                raise queue.Empty exception if the queue is empty.
                queue(False) function would do the same task also.
            '''
            #global processes
            #global tasks_to_accomplish
            task = tasks_to_accomplish.get_nowait()
            p = Process(target=func, args=(tgt,))
            processes.append(p)
            p.start()
        except queue.Empty:

            break
        else:
            '''
                if no exception has been raised, add the task completion
                message to task_that_are_done queue
            '''
            #global tasks_that_are_done
            tasks_that_are_done.put(task + ' is done by ' + current_process().name)
            time.sleep(.5)
    return True


def multi(func,tgt):

    tasks_to_accomplish.put(str(func))

    # creating processes
    #for w in range(NUM_WORKERS):
        #p = Process(target=do_job, args=(func,tgt,tasks_to_accomplish, tasks_that_are_done))
    p = Process(target=do_job, args=(func,tgt))
    processes.append(p)
    print(color.green('INFO: Starting '+tgt[0].module))
    p.start()

    # completing process
    for p in processes:
        p.join()

    # print the output
    # while not tasks_that_are_done.empty():
    #     print(tasks_that_are_done.get())

    return True