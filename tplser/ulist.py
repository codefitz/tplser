def uniq(lst):
    seen = set()
    seen_add = seen.add
    return [ x for x in lst if x not in seen and not seen_add(x)]