#这是一个nesterlee111.py模块，提供一个print_lol()函数，这个函数的作用是打印列表,其中可能是
#多重的嵌套列表

def print_lol(the_list,level):
#这个函数取两个位置参数，名为"the_list"、"level"，the_list参数这可以是任何python列表。所指定的列表中的
#每个数据项都会一一的输出到屏幕上，各数据项各占一行；而引入的"level"参数为函数的显示
#出具有缩进的数据组，函数会根据"level"的值提供满足条件的制表符

        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,level+1)
		else:
                        for tab_stop in range(level):
                                print("\t",end = '')

			print(each_item)
