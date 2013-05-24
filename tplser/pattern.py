import loops
import re

pattern_list = []

def pattern_parse(name, direction, line, num, end_num, eval, parse, err, line_num):
    if re.match("^\s*pattern\s\S+\s\d+\.\d", line):
        if direction:
            pname = re.findall("pattern\s(.*\s\d+\.\d)", line)
            name = pname[0]
            pattern_list.append(name)
            print (" Checking pattern... " + name)
            num += 1
            eval += 1
            parse = True
        else:
            num += 1
            eval -= 1
            eval = loops.loop_eval(eval, err, line_num)
            parse = False
    if re.match("^\s*end\spattern;", line):
        if direction:
            end_num += 1
            eval -= 1
            eval = loops.loop_eval(eval, err, line_num)
            parse = False 
        else:
            num += 1
            eval += 1
            parse = True
    return name, num, end_num, eval, parse, err, pattern_list