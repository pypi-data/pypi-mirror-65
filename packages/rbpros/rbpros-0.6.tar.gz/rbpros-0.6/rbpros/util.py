from typing import Dict, Type

pool: Dict[Type, int] = {}


def generate_id(klass: Type) -> str:
    global pool
    id = pool.get(klass)
    if not id:
        id = pool[klass] = 1
    else:
        id = pool[klass] = id+1
    return '%s_%s' % (klass.__name__, id)
