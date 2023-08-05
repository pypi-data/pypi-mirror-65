from collections import OrderedDict

from .utilities import get_logger


def get_stats(data, np_stats=['max', 'min', 'mean', 'std']):
    '''
    Given a numpy array, calculate all the numpy statistics and return them
    in a dictionary

    Args:
        data: Numpy array of any size/dimension
        np_stats: Statistic name to use, must be an function of a numpy array
    Returns:
        dictionary: dict of the stats names as keys and values associated with np_stats
    '''
    log = get_logger(__name__)

    # put together the operations to use
    operations = np_stats

    # Build the output
    out = OrderedDict()

    log.info('Data is {}'.format(' X '.join([str(s) for s in data.shape])))

    for op in operations:
        log.info('Calculating {} ...'.format(op))
        stat_fn = getattr(data, op)
        out[op] = stat_fn()

    return out
