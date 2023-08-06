from multiprocessing.pool import ThreadPool

from itertools import cycle, islice
import os


def run(cmd):
    print('run statement %s' % cmd)
    return cmd, os.system(cmd)


def run_statements_in_parallel(configuration, statements):
    pool = ThreadPool(configuration.parallel_tasks)
    for cmd, rc in pool.imap_unordered(run, statements):
        print('{cmd} return code: {rc}'.format(**vars()))

    pool.close()
    pool.join()
