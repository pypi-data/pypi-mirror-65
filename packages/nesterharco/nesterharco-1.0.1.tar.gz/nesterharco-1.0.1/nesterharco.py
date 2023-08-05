"""这是从Head First Python书里面照抄的。用于学习代码发布
版本测试
"""
import sys
def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1, fn)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t", end='', file=fn)
                        print(each_item, file=fn)
