"""
Python 内置方法学习、练习文件

参照官方文档的表格，分 4 天学习：
Day1 A-D
Day2 E-I
Day3 L-P
Day4 R-Z
"""

# Day1 A-D
# abs(x) 绝对值
print(abs(-1))  # 1
print(abs(10))  # 10
print(abs(0))  # 0

# aiter(async_iterable) 3.10 新功能 async 相关，对应普通的 iter()
# all(iterable) 所有的元素都为真值，返回 True 
print(all([1, 'True', set([1])]))  # True
print(all((0, True)))  # False

# any(iterable) 只要有一个为真，就返回 True
print(any([0, False, list(), {}]))  # False
print(any([True, False, False]))  # True

# awaitable anext(async_iterator[, default]) 为 next() 的异步版本
# ascii() 与 repr() 类似，表示对象的可打印的形式，并把非 ASCII 部分转为 Unicode 的数字形式
my_dict = {'A': '中', 'B': '文', 'C': 'ASCII'}
print(ascii(my_dict), repr(my_dict))  # {'A': '\u4e2d', 'B': '\u6587', 'C': 'ASCII'} {'A': '中', 'B': '文', 'C': 'ASCII'}

# bin(x) 将整数变成 `0b` 开头的二进制字符串，是一个合法的 Python 表达式
print(bin(3), bin(8))  # 0b11 0b1000

# class bool([x]) 返回 True or False，是 int 的子类不能再被继承
print(bool(0), bool([]), bool('False'), bool(object()))  # False False True True

# breakpoint(*args, **kws) 在代码里打断点
# class bytearray([source[, encoding[, errors]]]) 返回 bytes 数组，是可变序列
# bytes([source[, encoding[, errors]]]) 返回一个 bytes 对象，构造器，不可变对象

# callable(object) 如果参数 object 是可调用的就返回 True
def my_fn():
    pass

print(callable('a'), callable(abs), callable(my_fn))  # False True True

# chr(i) 将 Unicode 整数转成字符，ord() 的逆函数
print(ord('中'), chr(20013))  # 20013 中

# @classmethod() 装饰器，把一个方法变成类方法
class MyClass:
    @classmethod
    def my_class_method(cls):
        print('my_class_method')

MyClass.my_class_method()  # my_class_method

# compile(source, filename, mode, flag=0, dont_inherit=False, optimize=-1) 将字符串或者文件内容编译成 Python AST，不知道有什么作用，暂时不深入研究
# complex([real[, imag]]) 数学里的复数，不深入研究知道有这么个东西就可以了

# delattr(object, name) 从一个对象里删除一个属性，`delattr(obj, 'key')` 等价于 `del obj.key` 对应的方法是 setattr()
# dict() 字典构造器，这个可以在字典的学习中深入研究，这里带过
# dir([object]) 列出各种情况下的属性列表，对象可以通过 __dir__ 来实现，主要是为了便于在交互式时使用（IDE 环境下一般可以提示很多东西）
print(dir())  # ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'my_dict', 'my_fn']

# divmod(a, b) 等价于 (a // b, a % b) 同时返回除法的整数部分 + 余数部分，这个在有的时候很好用
print(divmod(5, 3), (5 // 3, 5 % 3))  # (1, 2) (1, 2)


