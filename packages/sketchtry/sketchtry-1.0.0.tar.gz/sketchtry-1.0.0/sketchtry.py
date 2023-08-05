# sketch.py模块提供两个异常处理机制，第一个机制是在尝试打开以sketch.txt命名的文件，若出现错误类型是
# IOError错误，则打印指定的字符串
#如果顺利找到以sketch.txt命名的文件，则使用迭代器来读取以data命名的数据，然后进入第二个异常处理
#机制,在打印一些对话类文本格式中，利用split()函数以“：”来分割，取另一参数1将来对话框中的对话
#分成两个部分，最后打印格式以“role said line_spoken”形式不换行打印；
#如遇到ValueError错误忽略，可以忽略。
try:
    
    data = open("sketch.txt")
    for each_line in data:
        try:
            (role, line_spoken) = each_line.split(":",1)
            print(role, end = "")
            print(" said: ", end = "")
            print(line_spoken, end = "")
        except ValueError:
            pass
    data.close()
except IOError:
    print("The data file is missing!")

    
