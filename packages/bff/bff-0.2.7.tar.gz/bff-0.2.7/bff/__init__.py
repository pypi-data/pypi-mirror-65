"""All of bff' functions."""
import logging

from ._version import get_versions

# Import submodules.
from . import plot

from .fancy import (
    avg_dicts,
    cast_to_category_pd,
    concat_with_categories,
    get_peaks,
    idict,
    kwargs_2_list,
    log_df,
    mem_usage_pd,
    normalization_pd,
    parse_date,
    pipe_multiprocessing_pd,
    read_sql_by_chunks,
    size_2_square,
    sliding_window,
    value_2_list,
)

from .config import FancyConfig

# Public object of the module.
__all__ = [
    'avg_dicts',
    'cast_to_category_pd',
    'concat_with_categories',
    'get_peaks',
    'idict',
    'kwargs_2_list',
    'log_df',
    'mem_usage_pd',
    'normalization_pd',
    'parse_date',
    'pipe_multiprocessing_pd',
    'plot',
    'read_sql_by_chunks',
    'size_2_square',
    'sliding_window',
    'FancyConfig',
    'value_2_list',
]


# Logging configuration.
FORMAT = '%(asctime)s [%(levelname)-7s] %(name)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

__version__ = get_versions()['version']
del get_versions
