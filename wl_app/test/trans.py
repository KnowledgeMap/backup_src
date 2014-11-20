# encoding: utf-8

import json, util, wrapper
from compiler.ast import Compare

nodes, links = [], []

graph = {}

class Node:
    def __init__(self, name, group):
        self.name = name.strip()
        self.group = group
        self.fuzzy = group
        self.mss = []
        
        self.vals = []
        self.edges = {}
    
    def __hash__(self):
        return self.name.__hash__()
    
    def __cmp__(self, other):
        return cmp(self.__hash__(), other.__hash__())
    
    def __str__(self):
        return self.__output__().__str__()
    
    def __repr__(self):
        return self.__str__()
    
    def __output__(self):
        if self.name.startswith(util.CENTER_PRE):
            return {'name':'', 'group':self.group}
        else:
            return {'name':self.name, 'group':self.group, 'fuzzy':self.fuzzy}
        
    def eval(self):
        if self.group > 1:
            return 0
        else:
            for val in self.vals:
                if eval(val):
                    return self.group ^ 1
            return self.group ^ 0
        
class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return obj.__output__()
        return json.JSONEncoder.default(self, obj)

def appendNode(name, group, label=[0]):
    '''
    str, str -> int
    '''
    global nodes
    global links
    
    def getGeneratedName():
        label[0] += 1
        return util.CENTER_TMP % (label[0])
    
    group = util.getGroup(group)
    
    if group > 1:
        name = getGeneratedName()
    if not name in nodes:
        nodes.append(Node(name, group))
    return name

def appendLink(func, params, flag):
    '''
    str, [str] -> None
    '''
    global nodes
    global links
    global graph
    
    params.append(appendNode('', func))
    params = map(lambda param:nodes.index(param), params)
    
    retval = util.fuzzy_induction(func, params)
    for param, edges in zip(params, retval):
        graph.setdefault(param, []).extend(edges)

    links += util.getLink(func, params)
    
    for index, val in zip(params[:-1], util.spread(func, params, flag)):
        nodes[index].vals.append(val)
        
vis = {}

def in_fuzzy(src):
    global vis, nodes, links, graph
    
    vis = {src:True}
    
    def areOkay(vs):
        def isOkay(v):
            if nodes[v].group:
                return True
            elif vis.get(v, False):
                return False
            else:
                return True
        for v in vs:
            if not isOkay(v):
                return False
        return True
    
    def isRecursive(v):
        if nodes[v].group:
            return False
        else:
            for vs in graph.setdefault(v, []):
                if areOkay(vs):
                    return True
            return False
        
    def compare(a, b):
        def count(vs):
#             print 'count', vs
            n, m = 0, 0
            for v in vs:
                if nodes[v].group:
                    n += 1
                else:
                    m += 1
            return n, m
        na, ma = count(a.get('mss', []))
        nb, mb = count(b.get('mss', []))
        if na > nb:
            return a
        elif na == nb and ma < mb:
            return a
        else:
            return b
        
        
    def DFS(u, deepth=0):
        retval = []
        
        if not isRecursive(u):
            if wrapper.__DEBUG__:
                print deepth * ' ', nodes[u].name, 'not recursive'
            return {'mss':[u]}
        
        for vs in graph.setdefault(u, []):
            if areOkay(vs):
                for v in vs:
                    if isRecursive(v):
                        vis[v] = True
                        temp = {'mss':list(set(vs) - set([v])), 'in':[v]}
                        dfs = DFS(v, deepth + 1)
                        temp.setdefault('mss', []).extend(dfs.get('mss', []))
                        temp.setdefault('in', []).extend(dfs.get('in', []))
                        if wrapper.__DEBUG__:
                            print temp
                        retval.append(temp)
                        vis[v] = False
                    else:
                        if wrapper.__DEBUG__:
                            print (deepth + 1) * ' ', nodes[v].name, nodes[v].group, '*'
                              
                retval += [{'mss':vs}]        
            
        for item in retval:
            for key in item:
                item[key] = list(set(item[key]))
        
        return reduce(compare, retval)
    
    dfs=DFS(src)
    _mss, _in = dfs.get('mss', []), dfs.get('in', [])
    _store = filter(lambda u:nodes[u].group == 1, _mss)
    _zero = filter(lambda u:nodes[u].group == 0, _mss)
    return {'store':_store, 'target':[src], 'zero':_zero, 'path':_in}

def fuzzy(src):
    '''
    int -> float
    '''
    
    global vis, nodes, links, graph
    
    vis = {src:True}
    
    def areOkay(vs):
        def isOkay(v):
            if nodes[v].group:
                return True
            elif vis.get(v, False):
                return False
            else:
                return True
        for v in vs:
            if not isOkay(v):
                return False
        return True
    
    def isRecursive(v):
        if nodes[v].group:
            return False
        else:
            for vs in graph.setdefault(v, []):
                if areOkay(vs):
                    return True
            return False
        
    def compare(a, b):
        def count(vs):
            n, m = 0, 0
            for v in vs:
                if nodes[v].group:
                    n += 1
                else:
                    m += 1
            return n, m
        na, ma = count(a)
        nb, mb = count(b)
        if na > nb:
            return a
        elif na == nb and ma < mb:
            return a
        else:
            return b

        
    def DFS(u, deepth=0):
        retval = []
        
        if not isRecursive(u):
            if wrapper.__DEBUG__:
                print deepth * ' ', nodes[u].name, 'not recursive'
            return [u]
        
        for vs in graph.setdefault(u, []):
            if areOkay(vs):
                for v in vs:
                    if isRecursive(v):
                        vis[v] = True
                        retval += [list(set(vs) - set([v])) + DFS(v, deepth + 1)]
                        vis[v] = False
                    else:
                        if wrapper.__DEBUG__:
                            print (deepth + 1) * ' ', nodes[v].name, nodes[v].group, '*'
                
                retval += [list(vs)]

        retval = map(set, retval)
        return list(reduce(compare, retval))
         
    dfs = DFS(src)
    return dfs

def fuzzy_value(vs):
    n, m = 0, 0
    for v in vs:
        if nodes[v].group:
            n += 1
        else:
            m += 1
    if n == 0 and m == 0:
        return 0
    else:
        return 1.0 * n / (n + m)

def fuzzyValue(v):
    if isinstance(v, basestring):
        v = nodes.index(v)
    vs = fuzzy(v)
    print nodes[v].name, map(lambda x:nodes[x].name, vs)
    return fuzzy_value(vs)
    
def parse(seq):
    '''
    str.json -> [node], [link]
    '''
    global nodes
    global links
    global graph
    
    data = json.loads(seq)
    _nodes, _funcs, _flag = data.get('nodes', []), data.get('funcs', []), data.get('flag', []).strip().lower()
    
    if _flag == 'deduction':
        _flag = util.DEDUCTION
    else:
        _flag = util.INDUCTION
    
    for node in _nodes:
        appendNode(node.get('name', []), node.get('group', []))
        
    for func in _funcs:
        appendLink(func.get('func', []), func.get('params', []), _flag)
        
    for key in graph:
        tmp = set([])
        for item in graph[key]:
            if item:
                tmp.add(tuple(item))
        graph[key] = tmp
        
    return nodes, links, _flag, data.get("target", False)

def dump(nodes, links, flag, param):
    '''
    [node], [link] -> str.json
    '''
    if flag == 'de':
        return json.dumps({"nodes":nodes, "links":links}, indent=4, cls=Encoder)
    else:
        return json.dumps({"nodes":nodes, "links":links, "info":param}, indent=4, cls=Encoder)
    
def clear():
    global nodes
    global links
    global graph
    nodes, links, graph = [], [], {}

if __name__ == '__main__':
    data = util.getInputData()
    n, l, f, t = parse(data)
