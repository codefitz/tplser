def tplfile(ext):
    if not ext.endswith(".tpl"):
        raise argparse.ArgumentTypeError("File must be of type *.tpl\n")
    return ext