def eval(eval, section):
    if (eval < 0):
        print (" * Missing module " + section + " opening statement!")
    if (eval > 0):
        print (" * Missing module end " + section + " statement!")