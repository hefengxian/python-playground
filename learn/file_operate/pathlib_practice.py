"""
这个文件是用来练习 pathlib 的，并且是在 macOS
"""

import os
from pathlib import PurePath, Path, PurePosixPath, PureWindowsPath, WindowsPath, PosixPath

# 首先要明白 PurePath & Path 的关系，以及对应的 Posix & Window 的关系
# PurePath 和 Path 的关系，PurePath 类似路径的字符串操作，并不涉及真正的操作文件，这意味着你在 Posix 系统上可以
# 使用 Windows 的，反之亦然
# 而 PurePath/Path 对应的两个 *PosixPath & *WindowsPath 主要是操作系统两大阵营具体的表现

# Path 相比于 PurePath 多了很多实际真正的文件操作，Path 继承于 PurePath
# 以上的这些都类都属于 os.PathLike 

p = PurePath(__file__)
print(type(p), isinstance(p, PurePosixPath))  # at macOS <class 'pathlib.PurePosixPath'> True
p = Path(__file__)
print(type(p), isinstance(p, PosixPath))  # at macOS <class 'pathlib.PosixPath'> True


# class PurePath(*pathsegments)
# 构造方法
# 参数为空表示当前路径 .
print(PurePath()) 
# 参数可以是字符串或者 os.PathLike
print(PurePath('/etc', 'apt', Path('apt.sourcelist'), PurePath('test')))  # /etc/apt/apt.sourcelist/test
# 多个根路径，只去最后那个
print(PurePath('/etc', '/usr', 'share'))  # /usr/share 这里前面的 /etc 就被忽略了

# 另外如果路径中间有多个斜杆或者单个点，会被折叠，具体是多个斜杆变成一个单点去掉
# 但是对于开头的 // 和 .. 是不处理的，这个在路径中本身就是有意义的
print(PurePath('A//B////C/./test.py'))  # A/B/C/test.py
print(PurePath('//host/mydir/../test.py'))  # //host/mydir/../test.py

# PurePath 在 Posix 系统下也可以实例化 Windows 的，反之亦然
print(PureWindowsPath('D:/Program Files/Python'))  # D:\Program Files\Python
print(PureWindowsPath('//host/share/file'))  # \\host\share\file


# 通用性质
# 路径是不可变，可哈希的；相同风格的可以排序和比较；遵循对应风格的大小写转换语义
print(PurePosixPath('foo') == PurePosixPath('Foo'))  # False
print(PureWindowsPath('foo') == PureWindowsPath('FoO'))  # True
print(PureWindowsPath('BaR') in [PureWindowsPath('baR')])  # True
print(PurePosixPath('foo') > PurePosixPath('bar'))  # True

# 不同风格不能相等，且不能排序比大小
print(PurePosixPath('foo') == PureWindowsPath('foo')) # False
# print(PurePosixPath('foo') > PureWindowsPath('bar'))  # TypeError: '>' not supported between instances of 'PurePosixPath' and 'PureWindowsPath'

# 运算符
# `/` 用于方便的创建子路径
print(PurePath('/usr') / 'share' / 'apache')

# 实例化对象可以用于任何支持 os.PathLike 实现的地方
print(os.fspath(PurePath('/usr/local/nginx')))

# 另外 str(PurePath) 会表示成路径对应系统下的表示法，比如 Windows 下的反斜杠
print(PureWindowsPath('c://Program Files'))  # c:\Program Files
print(PureWindowsPath('//host/share/myfile'))  # \\host\share\myfile
