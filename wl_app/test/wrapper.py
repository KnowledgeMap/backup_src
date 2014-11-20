# encoding: utf-8

import trans, util

class Wrapper:
    '''
    The only thing you need to know.
    '''
    def __init__(self, idata):
        '''
        @param idata: string TYPE, JSON FORMAT
            the data from front-end
        '''
        self.nodes, self.links, self.flag , self.target = trans.parse(idata)
        
    def iterateResult(self):
        '''
        generate the situation of next iteration.
        
        @return: string TYPE, JSON FORMAT
            next situation
        '''
        yield 
        while True:
            vals = [node.eval() for node in self.nodes]
            if not reduce(lambda x, y:x or y, vals):
                break
            else:
                for val, node in zip(vals, self.nodes):
                    if val:
                        node.group ^= 1
                yield
                
    def finalResult(self, maxSteps=-1):
        '''
        generate the situation after next maxSteps iteration(s).
        
        @param maxSteps: int TYPE
            -1 -> endless or stable
            other -> as you see
        @return: string TYPE, JSON FORMAT
            situation after next maxSteps iteration(s)
        '''
        
#         steps = 0
#         for val in self.iterateResult():
#             steps = steps + 1
#             if maxSteps != -1 and steps >= maxSteps:
#                 break
        
        
        if self.flag == util.DEDUCTION:
            for node in self.nodes:
                if not node.name.startswith(util.CENTER_PRE):
                    node.fuzzy = trans.fuzzyValue(node.name)
            retval = trans.dump(self.nodes, self.links, 'de', None)
        else:
            retval = trans.dump(self.nodes, self.links, 'in', trans.in_fuzzy(self.nodes.index(self.target)))
        
        trans.clear()
        return retval
    
__DEBUG__ = False

if __name__ == '__main__':
    idata = util.getInputData()
    wrapper = Wrapper(idata)
    print wrapper.finalResult()
