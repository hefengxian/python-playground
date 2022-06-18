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


# PurePath 属性
# PurePath.parts
print(PurePath('/etc/ssh/sshd.conf').parts)  # ('/', 'etc', 'ssh', 'sshd.conf')
print(PureWindowsPath('c:/windows/system32').parts)  # ('c:\\', 'windows', 'system32')

# PurePath.drive
print(PureWindowsPath('C:/Program Files/Python').drive)  # C:
print(PureWindowsPath('/Program Files/Python').drive)  # ''
print(PurePath('/usr').drive)  # ''
print(PureWindowsPath('//host/share/file.txt').drive)  # \\host\share

# PurePath.root
print(PureWindowsPath('C://windows').root)  # \
print(PureWindowsPath('c:windows').root)  # ''
print(PurePosixPath('/etc').root)  # /
print(PureWindowsPath('//host/share').root)  # \
print(PurePosixPath('//host/file').root)  # //
print(PurePosixPath('///etc').root)  # /
print(PurePosixPath('/////usr/share').root) # /

# PurePath.anchor 驱动器 + 根
print(PureWindowsPath('C:/Program Files').anchor)  # C:\
print(PureWindowsPath('c:windows').anchor)  # c:
print(PureWindowsPath('//host/share/text.txt').anchor)  # \\host\share\

# PurePath.parents 3.10 可以支持负索引切片
print(tuple(PureWindowsPath('c:/foo/bar/text.txt').parents))  # (PureWindowsPath('c:/foo/bar'), PureWindowsPath('c:/foo'), PureWindowsPath('c:/'))

# PurePath.parent 逻辑父路劲
print(PurePosixPath('/a/b/c/d').parent)  # /a/b/c
# 不能超过 anchor 或者空路径
print(PurePosixPath('/').parent)  # /
print(PurePosixPath('.').parent)  # .
# 这只是一个字符串运算而不能解析 `..`，只是路劲向后退一级
print(PurePosixPath('foo/../').parent)

# PurePath.name 最后路径的字符串，无论是目录还是文件
print(PurePosixPath('my/file/text.txt').name)  # text.txt
print(PurePosixPath('/etc/apt/').name)  # apt
# UNC 驱动器的目录不会被考虑（就是 host 后面的第一个路径，再之后的还是会被识别无论目录还是文件）
print(PureWindowsPath('//host/share/my.cnf').name)  # my.cnf
print(PureWindowsPath('//host/share').name)  # ''

# PurePath.suffix 单个后缀，是带点的
print(PurePath('file.mp4').suffix)  # .mp4
print(PurePath('file.tar.gz').suffix)  # .gz
print(PurePath('/etc/sudo').suffix)  # ''

# PurePath.suffixes
print(PurePath('file.tar.gz').suffixes)  # ['.tar', '.gz']
print(PurePath('/etc/profile').suffixes)  # []

# PurePath.stem 去掉后缀的名称
print(PurePath('/usr/share/mylog.log').stem)  # mylog
print(PurePath('/usr/profile').stem)  # profile

# PurePath 方法
# PurePath.as_posix()
print(PureWindowsPath('c:\\windows').as_posix())  # c:/windows

# PurePath.as_uri() 表示成 file URI 的模式，必须是绝对路径
# print(PureWindowsPath('Program Files/text.txt').as_uri())  # ValueError
print(PureWindowsPath('d:/Program Files').as_uri())  # file:///d:/Program%20Files
print(PurePosixPath('/etc/test.txt').as_uri())  # file:///etc/test.txt

# PurePath.is_absolute() 是否为绝对路径，这里指的是同时包含 驱动盘 + 根路径
print(PureWindowsPath('c://windows').is_absolute())  # True
print(PureWindowsPath('//host/share').is_absolute())  # True
print(PureWindowsPath('c:').is_absolute())  # False 没有包含根路径，只有驱动器
print(PurePosixPath('/c/b/d').is_absolute())  # True

# PurePath.is_relative_to(*other))  3.9 的新功能
print(PurePosixPath('/etc/passwd').is_relative_to('/etc'))  # True
print(PurePosixPath('/etc/passwd').is_relative_to('/usr'))  # False

# PurePath.is_reserved() 是否为被保留，这个POSIX总是返回 False 主要是 Windows
print(PureWindowsPath('nul').is_reserved())  # True
print(PurePosixPath('nul').is_reserved())  # False

# PurePath.joinpath(*other) 就是连接路径
print(PurePosixPath('/etc').joinpath('apt', PurePosixPath('apt.sourcelist')))  # /etc/apt/apt.sourcelist
print(PureWindowsPath('d:\\\\').joinpath('program files', 'Python'))  # d:\program files\Python

# PurePath.match(pattern) 需要注意绝对路径的 pattern 那么只能匹配绝对路径的，大小写是否敏感主要看平台
print(PurePath('a/b.py').match('*.py'))  # True
print(PurePath('/a/b/c.py').match('b/*.py'))  # True
print(PurePath('/a/b/c.py').match('/a/*.py'))  # False

print(PurePath('/a.py').match('/*.py'))  # True
print(PurePath('a/b.py').match('/*.py'))  # False

print(PurePosixPath('a.py').match('*.PY'))  # False
print(PureWindowsPath('a.PY').match('*.py'))  # True

# PurePath.relative_to(*other) 计算相对路径，如果不可计算抛出 ValueError
print(PurePosixPath('/etc/passwd').relative_to('/'))  # etc/passwd
print(PurePosixPath('/etc/passwd').relative_to('/etc'))  # passwd
# print(PurePosixPath('/ect/passwd').relative_to('/usr'))  # ValueError

# PurePath.with_name(name) 返回新名字的路径，如果原名字不存在会抛出 ValueError （文件重命名利器）
print(PureWindowsPath('c:/Users/Download/setup.py').with_name('setup.exe'))  # c:\Users\Download\setup.exe
# print(PureWindowsPath('c:/').with_name('text.txt'))  # ValueError

# PurePath.with_stem(stem)  3.9 新功能，返回新修改 stem 的路径，如果路径没有 stem 抛出 ValueError 多后缀的文件会损失掉多的后缀
print(PureWindowsPath('c:/Users/Download/test.py').with_stem('setup'))  # c:\Users\Download\setup.py
print(PurePosixPath('/home/user/data.tar.gz').with_stem('test'))  # /home/user/test.gz
# print(PureWindowsPath('c:/').with_stem('test'))  # ValueError

# PurePath.with_suffix(suffix) 修改后缀名，如果之前没有后缀那么会加上新的后缀，如果之前有后缀 suffix 为空字符串那么会移除后缀
print(PurePosixPath('/usr/share/test.pyc').with_suffix('.py'))  # /usr/share/test.py
print(PurePosixPath('text.tar.gz').with_suffix('.bz2'))  # text.tar.bz2
print(PurePath('README').with_suffix('.md'))  # README.md
print(PurePath('passwd.sh').with_suffix(''))  # passwd
