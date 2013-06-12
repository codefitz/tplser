'''
    A Function to strip comments "//" from functional lines within the pattern
    to evaluate the code.
'''
import re

def removal(line, double_quotes, single_quotes):
    # Strip comments
    if "//" in line:
        # This regex handles embedded " within ' quotes
        #values = re.findall("[\"\'].?.*?[\"\']", full_line)
        apos = line.find("'")
        dq = line.find('"')
        if apos > dq:
            values = re.findall(double_quotes, line) # Double quotes
        else:
            values = re.findall(single_quotes, line) # Single quotes
            
        if values: # if "//" is not a comment
            for val in values:
                if "//" in val:
                    line = line
                else:
                    line = line.split("//")[0]
        else:
            line = line.split("//")[0]
    else:
        line = line
        
    return line

'''
    A Function to ignore comment blocks.
'''
def noteblock(direction, comment, comment_line, line, open):
    if re.match(comment, line):
        if direction:
            if open > 0:
                ignore_text = False
                open -= 1
            else:
                ignore_text = True
                open += 1
            if re.search(comment_line, line):
                ignore_text = False
                open -= 1
        else:
            if re.match(comment_line, line):
                ignore_text = False
            if open == 0:
                ignore_text = True
                open += 1
            else:
                open -= 1
                ignore_text = False
                
        return ignore_text