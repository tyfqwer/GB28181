# 导入random模块
import random


# 定义一个函数，接受一个参数length，表示字符串的长度
def generate_random_string(length):
    result = ""
    for i in range(length):
        # 在每次循环中，使用random.randint(0,9)生成一个0到9之间的随机整数，并将其转换为字符串
        digit = str(random.randint(0, 9))
        # 将生成的数字字符串拼接到空字符串后面
        result += digit
    return result
