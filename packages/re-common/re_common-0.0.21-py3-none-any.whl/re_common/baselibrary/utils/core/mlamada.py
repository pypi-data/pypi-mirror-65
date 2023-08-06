# 通过传入的bool值确定是否打印string
printfunc = lambda LogBool, string: print(string) if LogBool else print("")

# 关闭r对象
closeResult = lambda r: r.close() if 'r' in locals() and r else None