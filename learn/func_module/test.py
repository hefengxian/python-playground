import os
import sys

from module1 import foo
foo()

from module2 import foo
foo()

if __name__ == '__main__':
    print(sys.version)
    print(sys.version_info)
    print(__file__)
    print(os.getcwd())

