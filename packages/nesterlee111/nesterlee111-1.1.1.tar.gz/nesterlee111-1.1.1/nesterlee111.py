#这是一个nesterlee111.py模块，提供一个print_lol()函数，这个函数的作用是打印列表,其中可能是
#多重的嵌套列表

import sys
def print_lol(the_list,indent = False ,level = 0,fh = sys.stdout):
#这个函数取四个位置参数，名为"the_list"、"indent"、"level"、"fh"，the_list参数这可以是任何python列表。所指定的列表中的
#每个数据项都会一一的输出到屏幕上，各数据项各占一行；
#indent参数默认给定缺省值False，不进行缩进，当需要将数据缩进打印显示时，给定True可以将数据缩进打印给出
#而引入的"level"参数为函数的打印显示制表符，函数会根据"level"的值提供满足条件的制表符
#最后给出fh参数，是用来标识将数据写入哪个位置，我们可以根据自己的喜好将打印数据写入某处，这里默认缺省值为sys.stdout

        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,level+1,fh)

                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end = "",file = fh)
                        print(each_item,file = fh)
