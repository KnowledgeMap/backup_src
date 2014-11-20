
import json
from wrapper import *


result = {}
#data = request.REQUEST['data']
data = '1001(a,b)\n10000011(b,c,d)\n10000011(d,e,f)\n10000011(f,g,h)\n10000011(h,i,j)\n10000011(j,k,l)'

lines = data.split('\n')

funcs = []
nodes = []
node_li = []

for i in lines:
    func_obj = {}
    
    func = i.split('(')[0]
    params = i.split('(')[1].replace(')','')
    params = params.split(',')
    
    func_obj['params'] = params
    func_obj['func'] = func
    funcs.append(func_obj)
    
    for p in params:
        if p not in node_li:
            node_li.append(p)
            node_info = {}
            node_info['group'] = '0'
            node_info['name'] = p
            nodes.append(node_info)

the_data = {}
the_data['funcs'] = funcs
the_data['nodes'] = nodes
the_data['flag'] = 'deduction'
#print the_data

the_data = json.dumps(the_data, indent=4)

wrapper = Wrapper(the_data)
the_str = wrapper.finalResult()

print the_str


wrapper = Wrapper(the_data)
the_str = wrapper.finalResult()

print the_str

wrapper = Wrapper(the_data)
the_str = wrapper.finalResult()

print the_str
