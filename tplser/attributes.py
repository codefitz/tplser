def open_requireds(pattern_name, line, count, eval, found, attr):
    count += 1
    eval += 1
    found.append(pattern_name)
    attr = False
    return count, eval, found, attr

def close_requireds(pattern_name, line, count, eval, missing, err, attr, missing_attr, attr_err):
    count += 1
    eval -= 1
    if (eval < 0):
        missing.append(pattern_name)
        eval = 0
        err += 1
    if not attr:
        missing_attr.append(pattern_name)
        attr_err += 1
    return count, eval, missing, err, missing_attr, attr_err

def closing_decs(eval, missing_end, pattern_name, err):
    if (eval > 0):
        missing_end.append(pattern_name)
        eval = 0
        err += 1
    return eval, missing_end, err