#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains auxiliary functions for parallelization.

Part of symenergy. Copyright 2018 authors listed in AUTHORS.
"""

import multiprocessing
from multiprocessing import Value, Lock
import numpy as np
import pandas as pd
import itertools
import time
from symenergy import _get_logger
from multiprocessing import current_process

from symenergy.auxiliary.params import RcParams

logger = _get_logger(__name__)


class MultiprocParams(RcParams):
    items_opts = {'nworkers':
                    {'types': {int: '>=0'},
                     'values': (None, False, 'default',),
                     'cond': 'int >= 0 or one of (None, False, "default")'},
                  'chunks_per_worker':
                      {'types': {int: '>=0'},
                       'values': (),
                       'cond': 'int >= 0'}}
    items_default = {'nworkers': 'default', 'chunks_per_worker': 2}

multiproc_params = MultiprocParams()


class Counter():
    def __init__(self):
        self.val = Value('f', 0)
        self.lock = Lock()

    def reset(self):
        with self.lock:
            self.val.value = 0

    def increment(self):
        with self.lock:
            self.val.value += 1

    def update_ema(self, newval):
        with self.lock:
            if self.val.value == 0:  # first run
                self.val.value = newval
            else:
                self.val.value = self.val.value * 0.99 + 0.01 * newval

    def value(self):
        with self.lock:
            return self.val.value


MP_COUNTER = Counter()
MP_EMA = Counter()


def log_time_progress(f):
    '''
    Decorator for progress logging.
    Note: Due to multiprocessing, this can't be used as an actual decorator.
    https://stackoverflow.com/questions/9336646/python-decorator-with-multiprocessing-fails
    Using explicit wrappers for each method instead.
    '''

    def wrapper(self, df, name, ntot, *args, **kwargs):
        t = time.time()
        res = f(df, *args, **kwargs)
        t = (time.time() - t)  / len(df)

        MP_EMA.update_ema(t)

        vals = (name, int(MP_COUNTER.value()), ntot,
                MP_COUNTER.value()/ntot * 100,
                len(df),
#                MP_EMA.value()/len(df)*1000,
#                t*1000 / len(df),
                current_process().name)
        logger.info(('{}: {}/{} ({:.1f}%), chunksize {}, {}').format(*vals))

        return res
    return wrapper


def get_default_nworkers():

    if multiproc_params['nworkers'] == 'default':
        return multiprocessing.cpu_count() - 1
    else:
        return multiproc_params['nworkers']


def parallelize_df(df, func, *args, nworkers='default', concat=True, **kwargs):
    MP_COUNTER.reset()
    MP_EMA.reset()

    logger.debug(str(('NWORKERS: ', multiproc_params['nworkers'])))
    logger.debug(f'args {args}, kwargs {kwargs}')

    nworkers = min(get_default_nworkers(), len(df))

    def split(df_):
        nchunks = min(nworkers * multiproc_params['chunks_per_worker'], len(df_))
        return np.array_split(df, nchunks)

    if isinstance(df, (pd.DataFrame, pd.Series)):
        df_split = split(df)
    elif isinstance(df, list) and isinstance(df[0], (pd.DataFrame, pd.Series)):
        df_split = df
    elif isinstance(df, list):
        df_split = split(df)
    else:
        raise ValueError('Unknown df argument type in parallelize_df')


    pool = multiprocessing.Pool(nworkers)
    if args or kwargs:
        args = itertools.product(df_split, list(args) + list(kwargs.values()))
        results = pool.starmap(func, args)
    else:
        results = pool.map(func, df_split)

    pool.close()
    pool.join()

    if isinstance(results[0], (list, tuple)):
        logger.info('parallelize_df: chaining ... ')
        results = list(itertools.chain.from_iterable(results))

    if isinstance(results[0], (pd.DataFrame, pd.Series)) and concat:
        logger.info('parallelize_df: concatenating ... ')
        results = pd.concat(results)

    logger.info('done.')
    return results



