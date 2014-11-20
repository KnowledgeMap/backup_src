# encoding: utf-8

import trans, util, wrapper

#data = util.getInputData()
#print data

data = '''
{
    "funcs": [
        {
            "params": [
                "\u97e9\u6885\u6885", 
                "b"
            ], 
            "func": "1001"
        }, 
        {
            "params": [
                "b", 
                "c", 
                "d"
            ], 
            "func": "10000011"
        }, 
        {
            "params": [
                "d", 
                "e", 
                "f"
            ], 
            "func": "10000011"
        }, 
        {
            "params": [
                "f", 
                "g", 
                "h"
            ], 
            "func": "10000011"
        }, 
        {
            "params": [
                "h", 
                "i", 
                "j"
            ], 
            "func": "10000011"
        }, 
        {
            "params": [
                "j", 
                "k", 
                "l"
            ], 
            "func": "10000011"
        }
    ], 
    "nodes": [
        {
            "group": "0", 
            "name": "\u97e9\u6885\u6885"
        }, 
        {
            "group": "0", 
            "name": "b"
        }, 
        {
            "group": "0", 
            "name": "c"
        }, 
        {
            "group": "0", 
            "name": "d"
        }, 
        {
            "group": "0", 
            "name": "e"
        }, 
        {
            "group": "0", 
            "name": "f"
        }, 
        {
            "group": "0", 
            "name": "g"
        }, 
        {
            "group": "0", 
            "name": "h"
        }, 
        {
            "group": "0", 
            "name": "i"
        }, 
        {
            "group": "0", 
            "name": "j"
        }, 
        {
            "group": "0", 
            "name": "k"
        }, 
        {
            "group": "0", 
            "name": "l"
        }
    ], 
    "flag": "induction", 
    "target": "b"
}
'''


wp1 = wrapper.Wrapper(data)
print wp1.finalResult()

wp2 = wrapper.Wrapper(data)
print wp2.finalResult()
