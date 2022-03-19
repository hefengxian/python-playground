"""
深入理解 slice 切片操作
"""

lst = list(range(10))

# X >= len(list) 时如下的切片都表示完整的 list（没有截取）
X = len(lst)
print(lst == lst[0:X])  # True
print(lst == lst[0:])  # True
print(lst == lst[:X])  # True
print(lst == lst[:])  # True
print(lst == lst[::])  # True
print(lst == lst[-X:X])  # True
print(lst == lst[-X:])  # True

print(lst[1:5])  # [1, 2, 3, 4]
print(lst[1:5:2])  # [1, 3]
print(lst[-1:])  # [9]
print(lst[-4:-2])  # [6, 7]
print(lst[:-2] == lst[-len(lst):-2] == [0, 1, 2, 3, 4, 5, 6, 7])  # True

# 步长为负时，其实并不是翻转列表，这个地方的表示如下

# 0 1 2 3 4 5 6 7 8 9
# ^ 到这里结束  <--   ^ 从这里开始
print(lst[::-1])  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 表示如下的截取方法
# 0 1 2 3 4 5 6 7 8 9
# ^  <--  ^
print(lst[4::-1])  # [4, 3, 2, 1, 0]

# 0 1 2 3 4 5 6 7 8 9
#   - ^   <--   ^ 注意这里 -9 的位置是开区间，所以取不到
print(lst[-3:-9:-1])  # [7, 6, 5, 4, 3, 2]

# 0 1 2 3 4 5 6 7 8 9
#   ^   ^   ^   ^   ^
print(lst[::-2])  # [9, 7, 5, 3, 1]

# 0 1 2 3 4 5 6 7 8 9
#         -   ^   ^
print(lst[-2:-6:-2])  # [8, 6]

lst = [1, 2, 3, 4]
my_lst = lst[::]
print(lst == my_lst)
# id() 方法， CPython 的实现返回的是内存地址
print(id(lst) == id(my_lst))

lst.append(['A', 'B'])
my_lst.extend([5, 6])
print(lst)  # [1, 2, 3, 4, ['A', 'B']]
print(my_lst)  # [1, 2, 3, 4, 5, 6]

# 一点没有用的操作，直接使用 len(lst) > 8 更好理解，效率更高
if lst[8:]:
    print('Length > 8')
else:
    print('Length <= 8')

# 切片只是浅拷贝
lst = [1, 2, [3, 4], 6]
my_lst = lst[:3]
print(my_lst)  # [1, 2, [3, 4]]
# 更新数据
lst[2].append('A')
print(my_lst)  # [1, 2, [3, 4, 'A']]

# 给切片赋值，注意：值必须是可迭代对象
lst = [1, 2, 3, 4]

# 头部添加
lst[:0] = [-1, 0]
print(lst)  # [-1, 0, 1, 2, 3, 4]

# 尾部添加
lst[len(lst):] = [6, 7]
print(lst)  # [-1, 0, 1, 2, 3, 4, 6, 7]

# 中间添加
lst[6:6] = [5]  # [-1, 0, 1, 2, 3, 4, 5, 6, 7]
print(lst)

# 必须是可迭代对象
# lst[:0] = 3  # TypeError: can only assign an iterable
lst[:0] = (-3, -2)
print(lst)  # [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]

# 前面我们操作的都是：切片后列表是空的
# 那么切片后的列表不为空，复制后之后会发生什么？—— 替换
lst = [0, 1, 2, 5]
lst[3:] = (3, 4, 5)
print(lst)  # [0, 1, 2, 3, 4, 5]

lst[2:4] = ['A', 'B']
print(lst)  # [0, 1, 'A', 'B', 4, 5]

# 不等长的替换
lst[2:4] = ['x'] * 4
print(lst)  # [0, 1, 'x', 'x', 'x', 'x', 4, 5]

# 删除
del lst[2:6]
print(lst)  # [0, 1, 4, 5]

# 使用自定义步长的替换，注意：带步长的只能等长替换
lst = [0, 1, 2, 3, 4, 5]

lst[::2] = ['A', 'B', 'C']
print(lst)  # ['A', 1, 'B', 3, 'C', 5]

lst[::2] = ['X'] * 3
print(lst)  # ['X', 1, 'X', 3, 'X', 5]

# lst[::2] = ['W']  # ValueError: attempt to assign sequence of size 1 to extended slice of size 3

del lst[::2]
print(lst)  # [1, 3, 5]


# 自定义切片对象
class MyList:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, key):
        print(f"Key is: {key}")
        if isinstance(key, slice):
            return self.data[key]
        elif isinstance(key, int):
            return self.data[key]
        else:
            msg = f"{MyList.__name__} indices must be integers"
            raise TypeError(msg)


ml = MyList([1, 2, 3, 4])
print(ml[1])
print(ml[:2])
print(ml['key'])
# 输出如下：
# Key is: 1
# 2
# Key is: slice(None, 2, None)
# [1, 2]
# Key is: key
# Traceback (most recent call last):
#   ...
# TypeError: MyList indices must be integers
