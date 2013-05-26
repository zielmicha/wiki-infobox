from lxml.cssselect import CSSSelector

from tools import *

__all__ = ['get_infobox']

def get_raw_infobox_map(elem):
    boxes = CSSSelector('table.infobox')(elem)
    if not boxes:
        return []
    box = boxes[0]
    map = []
    for row in box.findall('tr'):
        cells = CSSSelector('td, th')(row)
        if len(cells) == 2:
            key, value = cells
            map.append((key, value))
    return map

def translate_key(elem):
    return [ i.strip() for i in mstringify_children(elem).split(',') ]

def mstringify_children(elem):
    return stringify_children(elem).replace(u'\xa0', ' ')

def translate_value(elem):
    val = mstringify_children(elem)
    first_val = val.split()[0] if val else ''
    try:
        return int(first_val), val
    except ValueError:
        try:
            return float(first_val), val
        except ValueError:
            return val

def get_infobox(elem):
    if isinstance(elem, basestring):
        return get_infobox(fetch_html(elem))
    m = {}
    for raw_k, raw_v in get_raw_infobox_map(elem):
        for k in translate_key(raw_k):
            m[k] = translate_value(raw_v)
    return m

def get(name):
    m = get_infobox(name)
    result = DictObject()
    for k, v in m.items():
        k = k.lower().replace("'", '').replace(' ', '_')
        if isinstance(v, tuple):
            setattr(result, k, v[0])
            setattr(result, k + '_full', v[1])
        else:
            setattr(result, k, v)
    return result

class DictObject(object):
    pass

if __name__ == '__main__':
    import pprint
    box = get_infobox('http://en.wikipedia.org/wiki/Caesium')
    pprint.pprint(box)
