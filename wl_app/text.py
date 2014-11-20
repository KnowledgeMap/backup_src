# encoding: utf-8

import trans, util, wrapper

#data = util.getInputData()
#print data

data = '''
{
    "funcs": [
        {
            "params": [
                "A", 
                "B", 
                "C"
            ], 
            "func": "10000011"
        }, 
        {
            "params": [
                "C", 
                "D", 
                "A"
            ], 
            "func": "10001011"
        }, 
        {
            "params": [
                "E", 
                "D", 
                "F"
            ], 
            "func": "11001011"
        }
    ], 
    "nodes": [
        {
            "group": "0", 
            "name": "A"
        }, 
        {
            "group": "0", 
            "name": "B"
        }, 
        {
            "group": "0", 
            "name": "C"
        }, 
        {
            "group": "0", 
            "name": "D"
        }, 
        {
            "group": "1", 
            "name": "E"
        }, 
        {
            "group": "0", 
            "name": "F"
        }
    ], 
    "flag": "induction", 
    "target": "D"
}
'''


wp1 = wrapper.Wrapper(data)
print wp1.finalResult()

#wp2 = wrapper.Wrapper(data)
#print wp2.finalResult()
