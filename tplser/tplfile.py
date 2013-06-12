'''
    Check for tpl file extension.
'''
def tplfile(ext):
    if not ext.endswith(".tpl"):
        raise argparse.ArgumentTypeError("File must be of type *.tpl\n")
    return ext
    
'''
    Evaluate each line and assign it values in order to decide how it is parsed.
'''
class Line(object):
    def __init__(self, actual, line_num, type):
        self.actual = actual
        self.line_num = line_num
        self.type = type
        
        '''
        Types:
        
        blank
        variable
        model statement
        import statement
        module statement
        overrides statement
        if statement
        trigger statement
        log statement
        search function
        definitions statement
        break
        continue
        stop
        tags
        regex function
        discovery function
        tpl declaration
        identify
        constants
        pattern declaration
        body declaration
        table declaration
        configuration declaration
        metadata declaration
        define declaration
        overview declaration
        for statement
        '''