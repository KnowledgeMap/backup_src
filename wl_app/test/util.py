# encoding: utf-8

import re, json

CENTER_PRE = '__center__-'
CENTER_TMP = CENTER_PRE + '(%d)'

def getGroup(func):
    '''
    str -> int
    '''
    if not isinstance(func, basestring):
        raise Exception('excepted str, while gets int.')
    
    if func == '0':
        return 0
    elif func == '1':
        return 1
    elif func == '11':
        return 2
    elif func == '1001':
        return 3
    elif func == '1011':
        return 4
    elif func == '10000011':
        return 5
    elif func == '11000001':
        return 6
    elif func == '11100001':
        return 7
    elif func == '10001011':
        return 8
    elif func == '11101001':
        return 9
    elif func == '11001011':
        return 10
    elif func == '10001111':
        return 11
    elif func == '11101011':
        return 12
    elif func == '11101111':
        return 13
    else:
        raise IndexError('not support this boolean function yet.')
    
def getLink(func, params):
    '''
    str, [int] -> [dict]
    '''
    retval = []
    for param in params[:-1]:
        retval.append({"source":param, "target":params[-1]})
    return retval

def deduction(func, params):
    '''
    str, [int] -> [dict]
    '''
    def _deduction_(func, params):
        '''
        str, [int] -> str(eval)
        '''
        if func == '11':
            for exp in ['{A}']:
                yield exp.format(A=params[0])
        elif func == '1001':
            for exp in ['{A} or {B}', '{A} or {B}']:
                yield exp.format(A=params[0], B=params[1])
        elif func == '1011':
            for exp in ['{A}', '{A} or {B}']:
                yield exp.format(A=params[0], B=params[1])
        elif func == '10000011':
            for exp in ['{A}', '{A} or {B} or {C}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11000001':
            for exp in ['{A} or {B} or {C}', '{B} or {C}', '{B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11100001':
            for exp in ['{A} or {C}', '{B} or {C}', '({A} and {B}) or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '10001011':
            for exp in ['{A}', '{A} or {B}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101001':
            for exp in ['({B} and {C}) or {A}', '({A} and {C}) or {B}', '({A} and {B}) or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11001011':
            for exp in ['{A}', '({A} and {C}) or {B}', '{B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '10001111':
            for exp in ['{A}', '{B}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101011':
            for exp in ['{A}', '({A} and {C}) or {B}', '({A} and {B}) or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101111':
            for exp in ['{A}', '{B}', '({A} and {B}) or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        else:
            raise Exception('no such boolean function, deduction')
    
    retval = []
    for exp in _deduction_(func, params):
        retval.append('(' + exp + ')')
    return retval

def fuzzy_induction(func, params):
    '''
    str, [int] -> [[int]]
    '''
    
    def split(flag, params, skip):
        retval = []
        for i, v in enumerate(flag):
            if i == skip:
                continue
            elif v == 'T':
                retval.append(params[i])
        return retval
    
    A = lambda flag, params:split(flag, params, 0)
    B = lambda flag, params:split(flag, params, 1)
    C = lambda flag, params:split(flag, params, 2)
    

    def _fuzzy_induction_(func, params):
        if func == '11':
            for a in ['I']:
                yield [A(a, params)]
        elif func == '1001':
            for a in ['TT']:
                for b in ['TT']:
                    yield [A(a, params), B(b, params)]
        elif func == '1011':
            for a in ['TI']:
                for b in ['TT']:
                    yield [A(a, params), B(b, params)]
        elif func == '10000011':
            for a in ['TII']:
                for b in ['TTI', 'ITT']:
                    for c in ['TIT', 'ITT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11000001':
            for a in ['TIT', 'TTI']:
                for b in ['ITT']:
                    for c in ['ITT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11100001':
            for a in ['TIT']:
                for b in ['ITT']:
                    for c in ['TTT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '10001011':
            for a in ['TII']:
                for b in ['TTI']:
                    for c in ['TIT', 'ITT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11101001':
            for a in ['TTT']:
                for b in ['TTT']:
                    for c in ['TTT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11001011':
            for a in ['TII']:
                for b in ['TTT']:
                    for c in ['ITT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '10001111':
            for a in ['TII']:
                for b in ['ITI']:
                    for c in ['ITT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11101011':
            for a in ['TII']:
                for b in ['TTT']:
                    for c in ['TTT']:
                        yield [A(a, params), B(b, params), C(c, params)]
        elif func == '11101111':
            for a in ['TII']:
                for b in ['ITI']:
                    for c in ['TTI']:
                        yield [A(a, params), B(b, params), C(c, params)]
        else:
            raise Exception('no such boolean function, induction')
    
    tmp = {}
    for vs in _fuzzy_induction_(func, params):
        for i, v in enumerate(vs):
            tmp.setdefault(i, []).append(v)
            
    retval = []
    for key in range(len(tmp)):
        retval.append(tmp[key])
        
#     print retval
    return retval
    
#     print '--', func, params
    

def induction(func, params):
    '''
    str, [int] -> [dict]
    '''
    def _induction_(func, params):
        '''
        str, [int] -> str(eval)
        '''
        if func == '11':
            for exp in ['{A}']:
                yield exp.format(A=params[0])
        elif func == '1001':
            for exp in ['{A} or {B}', '{A} or {B}']:
                yield exp.format(A=params[0], B=params[1])
        elif func == '1011':
            for exp in ['{A} or {B}', '{A}']:
                yield exp.format(A=params[0], B=params[1])
        elif func == '10000011':
            for exp in ['{A} or {B} or {C}', '{B} or {C}', '{B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11000001':
            for exp in ['{A}', '{A} or {B} or {C}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11100001':
            for exp in ['{A} or {C}', '{B} or {C}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '10001011':
            for exp in ['{A} or {B} or {C}', '{B} or {C}', '{C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101001':
            for exp in ['{A} or {B} or {C}', '{A} or {B} or {C}', '{A} or {B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11001011':
            for exp in ['{A} or {B}', '{B} or {C}', '{B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '10001111':
            for exp in ['{A} or {C}', '{B} or {C}', '{C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101011':
            for exp in ['{A} or {B} or {C}', '{B} or {C}', '{B} or {C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        elif func == '11101111':
            for exp in ['{A} or {C}', '{B} or {C}', '{C}']:
                yield exp.format(A=params[0], B=params[1], C=params[2])
        else:
            raise Exception('no such boolean function, induction')
    
    retval = []
    for exp in _induction_(func, params):
        retval.append('(' + exp + ')')
    return retval

DEDUCTION = 0
INDUCTION = 1

def spread(func, params, flag):
    '''
    str, [int], int -> [str]
    '''
    retval = []
    if flag == DEDUCTION:
        retval = deduction(func, params)
    elif flag == INDUCTION:
        retval = induction(func, params)
    else:
        raise Exception('only deduction or induction')  
    return map(lambda exp:re.sub(r'(\d+)', r'nodes[\1].group', exp), retval)

#===============================================================================
# input data generator, FOR TEST ONLY
#===============================================================================

nodes, funcs = [], []

nodes.append({"name":"a=b", "group":'1'})
nodes.append({"name":"a=c", "group":'0'})
nodes.append({"name":"b=c", "group":'0'})
nodes.append({"name":"a=e", "group":'0'})
nodes.append({"name":"b=e", "group":'0'})
nodes.append({"name":"c=e", "group":'0'})

funcs.append({"func":"11101001", "params":["a=b", "a=c", "b=c"]})
funcs.append({"func":"11101001", "params":["a=b", "a=e", "b=e"]})
funcs.append({"func":"11101001", "params":["b=e", "c=e", "b=c"]})
funcs.append({"func":"11101001", "params":["a=c", "a=e", "c=e"]})

def getInputData(data={"nodes":nodes, "funcs":funcs, "flag":"induction", "target":"c=e"}):
    return json.dumps(data, indent=4)

if __name__ == '__main__':
    print getInputData()
