from collections import defaultdict
from itertools import chain
from operator import methodcaller


def merge_dict_list(*dicts) -> dict:
    # initialise defaultdict of lists
    dd = defaultdict(list)

    # iterate dictionary items
    dict_items = map(methodcaller('items'), dicts)
    for k, v in chain.from_iterable(dict_items):
        dd[k].extend(v)

    return {k: v for k, v in dd.items()}
