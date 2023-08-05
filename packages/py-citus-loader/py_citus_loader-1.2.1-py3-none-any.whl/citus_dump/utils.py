from multiprocessing.pool import ThreadPool

from itertools import cycle, islice
import os

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    num_active = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while num_active:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            # Remove the iterator we just exhausted from the cycle.
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))


def run(cmd):
    print('run statement %s' % cmd)
    return cmd, os.system(cmd)


def run_statements_in_parallel(configuration, statements):
    pool = ThreadPool(configuration.parallel_tasks)
    for cmd, rc in pool.imap_unordered(run, statements):
        print('{cmd} return code: {rc}'.format(**vars()))

    pool.close()
    pool.join()
