
from ctypes import *

test = CDLL('test.dll')
test.wtmsb(c_double(3959),c_int(10959),c_int(2100000),c_double(230),c_double(205),c_double(0.9983),c_double(0.9971),c_double(0.9955))

