# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
import json
import traceback
from wrapper import *

def index(request):
    
    return HttpResponseRedirect('index.html')

def start_layout(request):
    result = {}
    try:
        
        data = request.REQUEST['data']
        #data = '1001(a,b)\n10000011(b,c,d)\n10000011(d,e,f)\n10000011(f,g,h)\n10000011(h,i,j)\n10000011(j,k,l)'
        
        lines = data.split('\n')
        
        funcs = []
        nodes = []
        node_li = []
        
        for i in lines:
            if '(' in i and ')' in i:
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
                        #print node_info['name']
                        #print p
                        #print p.encode('utf-8')
                        nodes.append(node_info)
        
        the_data = {}
        the_data['funcs'] = funcs
        the_data['nodes'] = nodes
        the_data['flag'] = 'deduction'
        #print nodes
        the_data = json.dumps(the_data, indent=4)
        #print 'start-------'
        #print the_data
        wrapper = Wrapper(the_data)
        #print '----'
        the_str = wrapper.finalResult()
        #print '===='
        #print the_str
        s3 = '''{"res": "right", "data":''' + the_str + '''}'''
        #print the_str.decode('utf-8')
        #print the_str.decode('gbk')
        #print the_str.encode('utf-8')
        #print the_str.encode('gbk')
        #print type(the_str)
        #print the_str.decode("gbk").encode("gbk")
        result['res'] = 'right'
        result['data'] = eval(the_str)
        #print json.dumps(result,ensure_ascii=False)
        #print result['data']['nodes']
        #for i in result['data']['nodes']:
        #    #print i['name']
        #    print i['name'].encode('utf-8')
        #    print i['name'].encode('gbk')
        #    print i['name'].decode('utf-8')
        #    print i['name'].decode('gbk')
        #    print i['name'].decode("utf-8").encode("gbk")
        #print result['data']
        #print '-------end'
        
        #s1 = json.dumps(result).decode('utf-8').encode('gbk')
        #s2 = '''{"res": "right", "data": {"nodes": [{"group": 0, "name": "\\u97e9\\u6885\\u6885"}, {"group": 0, "name": "b"}, {"group": 0, "name": "c"}, {"group": 0, "name": "d"}, {"group": 0, "name": "e"}, {"group": 0, "name": "f"}, {"group": 0, "name": "g"}, {"group": 0, "name": "h"}, {"group": 0, "name": "i"}, {"group": 0, "name": "j"}, {"group": 0, "name": "k"}, {"group": 0, "name": "l"}, {"group": 3, "name": ""}, {"group": 5, "name": ""}, {"group": 5, "name": ""}, {"group": 5, "name": ""}, {"group": 5, "name": ""}, {"group": 5, "name": ""}], "links": [{"source": 0, "target": 12}, {"source": 1, "target": 12}, {"source": 1, "target": 13}, {"source": 2, "target": 13}, {"source": 3, "target": 13}, {"source": 3, "target": 14}, {"source": 4, "target": 14}, {"source": 5, "target": 14}, {"source": 5, "target": 15}, {"source": 6, "target": 15}, {"source": 7, "target": 15}, {"source": 7, "target": 16}, {"source": 8, "target": 16}, {"source": 9, "target": 16}, {"source": 9, "target": 17}, {"source": 10, "target": 17}, {"source": 11, "target": 17}]}}'''
        #print type(s1)
        #print s1
        #print type(s2)
        #print s2
        #return HttpResponse(s2)
        
        return HttpResponse(s3)
        
    except Exception, e:
        #print str(e)
        print traceback.format_exc()
        result['res'] = 'wrong'
        result['data'] = traceback.format_exc()
        return HttpResponse(json.dumps(result))

def get_node_dic(node_str):
    node_dic = {}
    
    node_li = node_str[:-4].split('----')
    for n in node_li:
        node_name = n.split('====')[0]
        node_group = n.split('====')[1]
        
        node_dic[node_name] = node_group
    
    return node_dic

def start_change(request):
    result = {}
    try:
        data = request.REQUEST['data']
        node_str = request.REQUEST['node_str']
        flag = request.REQUEST['flag']
        target_name = request.REQUEST['target_name']
        
        node_dic = get_node_dic(node_str)
        lines = data.split('\n')
        funcs = []
        nodes = []
        node_li = []
        
        if flag == 'induction':
            store_name = request.REQUEST['store_name']
            for i in lines:
                func_obj = {}
                
                func = i.split('(')[0]
                params = i.split('(')[1].replace(')','')
                params = params.split(',')
                
                func_obj['params'] = params
                func_obj['func'] = func
                funcs.append(func_obj)
                
                # 图方便，在这直接改了，也可以从node_str那重新声场
                for p in params:
                    if p not in node_li:
                        node_li.append(p)
                        node_info = {}
                        #node_info['group'] = node_dic[p]
                        if p == target_name or p == store_name:
                            node_info['group'] = '1'
                        else:
                            node_info['group'] = '0'
                        node_info['name'] = p
                        nodes.append(node_info)
            
            the_data = {}
            the_data['funcs'] = funcs
            the_data['nodes'] = nodes
            the_data['flag'] = flag
            the_data['target'] = target_name
        # deduction
        else:
            for i in lines:
                func_obj = {}
                
                func = i.split('(')[0]
                params = i.split('(')[1].replace(')','')
                params = params.split(',')
                
                func_obj['params'] = params
                func_obj['func'] = func
                funcs.append(func_obj)
                
                # 图方便，在这直接改了，也可以从node_str那重新声场
                for p in params:
                    if p not in node_li:
                        node_li.append(p)
                        node_info = {}
                        
                        if p == target_name:
                            node_info['group'] = '1'
                        else:
                            node_info['group'] = '0'
                        node_info['name'] = p
                        nodes.append(node_info)
            
            the_data = {}
            the_data['funcs'] = funcs
            the_data['nodes'] = nodes
            the_data['flag'] = flag
        
        the_data = json.dumps(the_data, indent=4)
        #print the_data
        wrapper = Wrapper(the_data)
        the_str = wrapper.finalResult()
        
        s3 = '''{"res": "right", "data":''' + the_str + '''}'''
        return HttpResponse(s3)
    except Exception, e:
        #print str(e)
        print traceback.format_exc()
        result['res'] = 'wrong'
        result['data'] = traceback.format_exc()
        return HttpResponse(json.dumps(result))