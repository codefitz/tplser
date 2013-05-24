def open_match(count, eval):
    count += 1
    eval += 1
    return count, eval

def close_match(count, eval):
    count += 1
    eval -= 1
    return count, eval