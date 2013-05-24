import loops
import re

def body_parse(direction, line, num, end_num, eval, parse, err, line_num):
    if re.match("^\s*body\s*$", line):
        if direction:
            num += 1
            eval += 1
            parse = True
        else:
            num += 1
            eval -= 1
            eval = loops.loop_eval(eval, err, line_num)
            parse = False
    elif re.match("^\s*end\sbody;", line):
        if direction:
            end_num += 1
            eval -= 1
            eval = loops.loop_eval(eval, err, line_num)
            parse = False
        else:
            num += 1
            eval += 1
            parse = True
    return num, end_num, eval, parse, err