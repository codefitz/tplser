'''
    Evaluate single line sections.
'''
def eval(eval, section):
    if (eval < 0):
        print (" * Missing module " + section + " opening statement!")
    if (eval > 0):
        print (" * Missing module end " + section + " statement!")

'''
    Check evaluation for inside section or not.
'''
def loop_eval(eval, err, line):
    if eval < 0:
        err.append(line)
        eval = 0
    return eval, err

'''
    Function to warn if section is missing or syntax wrong
'''
def missing_warn(section, missing, missing_end, err, end_err, count, pattern_num, pattern_list, has_it):
    if (missing or missing_end):
        if err > 0:
            print(" * Missing " + section + " declaration(s)...")
            print_patt(missing)
        if end_err > 0:
            print(" * Missing closing " + section + " declaration(s)...")
            print_patt(missing_end)
    elif (count < pattern_num):
        print (" * " + section + " section missing!")
        for pattern in pattern_list:
            if pattern not in has_it:
                print ("    Pattern: " + str(pattern))

'''
    Uniq a list.
'''
def uniq(lst):
    seen = set()
    seen_add = seen.add
    return [ x for x in lst if x not in seen and not seen_add(x)]

'''
    Print a warning.
'''
def warnings(list, warning):
    print "\n * " + warning + ":"
    for var in list:
        print ("    line " + str(var))
    print "\r"