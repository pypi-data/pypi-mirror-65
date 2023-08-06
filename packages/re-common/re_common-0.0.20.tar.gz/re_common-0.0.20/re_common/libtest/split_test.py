from re_common.baselibrary.tools.split_line_2_many import Split_2_lines

def splite_test():
    infilepath = r''
    outfilepath = r''
    spli = Split_2_lines()
    spli.split_line(infilepath,
                    "\"}",
                    outfilepath)

if __name__ == '__main__':
    splite_test()