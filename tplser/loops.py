def loop_eval(eval, err, line):
    if eval < 0:
        err.append(line)
        eval = 0
    return eval