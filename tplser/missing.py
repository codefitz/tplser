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