from npc_internal.logger import logger


_proxy_ids = {}


def is_proxy(obj):
    return id(obj) in _proxy_ids


def get_proxy_id(obj):
    tpl = _proxy_ids.get(id(obj))
    if tpl:
        proxy_id = tpl[0]
    else:
        proxy_id = None
    logger.debug('Returning proxy id %s (%s) -> %s' % (id(obj), type(obj), proxy_id))
    return proxy_id


def set_proxy_id(obj, proxy_id):
    global _proxy_ids
    # logger.debug('Setting proxy id %s (%s) -> %s' % (id(obj), type(obj), proxy_id))

    # TODO: this next line is a giant hack. we keep a reference to "obj" around
    # in the tuple to ensure that it doesn't get garbage collected, thus ensuring
    # unique-ness of id(obj). However, this also results in memory leaks. Revisit
    # this. Figuring out how to associated proxy ID's with objects is a bit
    # tricky.
    _proxy_ids[id(obj)] = (proxy_id, obj)

