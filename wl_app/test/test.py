# encoding: utf-8

import util, wrapper

data = util.getInputData()

wp1 = wrapper.Wrapper(data)
data_1 = wp1.finalResult()
print data_1

wp2 = wrapper.Wrapper(data)
data_2 = wp2.finalResult()
print data_2

print data_1 == data_2

print {'a':1}&{'b':2}
