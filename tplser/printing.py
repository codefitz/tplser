def print_eval(section, open, close, clause, err, rev_err):
    if (open == close):
        print (" * Even number of " + clause + " (" + str(open) + "), but you've done something really wrong...")
        print ("   (Check closing statements across patterns/bodys.)")
    else:
        print (" * Odd number of " + clause + " found! " + str(section) + " = " + str(open) + "; end " + str(section) + " = " + str(close) +":")

    if (err):
        for line_err in err:
            print ("   line " +str(line_err) + ": " + clause + " here or inside missing opening statement.")
    if (rev_err):
        for line_err in rev_err:
            print ("   line " +str(line_err) + ": " + clause + " here or inside missing closing statement.")
    print "\n"