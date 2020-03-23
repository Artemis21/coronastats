from datetime import datetime, timedelta
from copy import deepcopy
import discord


CACHE = {}


def cache(func):
    def wrapper(*args):
        name = f'{func.__name__}{repr(args)}'
        if name in CACHE:
            entry = CACHE[name]
            if entry[0] > datetime.now()-timedelta(hours=1):
                if entry[2]:
                    file = deepcopy(entry[2])
                    res = dict(entry[1])
                    res['file'] = discord.File(file, filename='graph.png')
                else:
                    res = entry[1]
                return res
            else:
                del CACHE[name]
        result = func(*args)
        if 'b_io' in result:
            b_io = result['b_io']
            del result['b_io']
        else:
            b_io = None
        CACHE[name] = [datetime.now(), result, b_io]
        return result
    return wrapper
