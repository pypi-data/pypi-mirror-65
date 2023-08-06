from .interface import Template,VCategory,Simplification
from .tensor import V,constant
from .op import MM,SliceSelect
class TemplateConstant(Template):
    active_operator = None

    def simplify(self, symbol: V):
        if symbol.is_operator():
            for s in symbol.input:
                if not s.is_constant():
                    return False
            compute_inputs = [_s.value for _s in symbol.input]
            value = symbol.operator.f(*compute_inputs)
            symbol.clear_operator()
            symbol.value = value
            symbol.category = VCategory.constant
            symbol.name=None
            return True
        else:
            return False


class TemplatePlus(Template):
    from trik.sheng.op import Plus
    active_operator = Plus

    def simplify(self, symbol: V):
        from trik.sheng.op import Mul,Broadcast
        left_symbol, right_symbol = symbol.input
        if left_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
            self.reduce_symbol(symbol, 1)
            return True
        elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 0):
            self.reduce_symbol(symbol, 0)
            return True
        elif self.symbol_equal(left_symbol, right_symbol):
            symbol.clear_operator()
            symbol.symbolic_compute(Mul(), [left_symbol, constant(2)])
            symbol.name=None
            return True
        elif left_symbol.operator!=None: 
            if left_symbol.operator.operator_sign=='-' and left_symbol.operator.inputs_count==1 and self.symbol_equal(left_symbol.input[0],right_symbol):
                symbol.clear_operator()
                symbol.symbolic_compute(Broadcast(()),[constant(0)])
                symbol.name=None
                return True
        elif right_symbol.operator!=None: 
            if right_symbol.operator.operator_sign=='-' and left_symbol.operator.inputs_count==1 and self.symbol_equal(right_symbol.input[0],left_symbol):
                symbol.clear_operator()
                symbol.symbolic_compute(Broadcast(()),[constant(0)])
                symbol.name=None
                return True
        else:
            return False


class TemplateSubtract(Template):
    from trik.sheng.op import Sub
    active_operator = Sub

    def simplify(self, symbol: V):
        from trik.sheng.op import Neg,Broadcast#SliceAssign
        left_symbol, right_symbol = symbol.input
        if right_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
            symbol.clear_operator()
            symbol.clear_input()
            symbol.symbolic_compute(Neg(), [right_symbol])
            symbol.name=None
            return True
        elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 0):
            self.reduce_symbol(symbol, 0)
            return True
        elif self.symbol_equal(left_symbol, right_symbol):
            symbol.clear_operator()
            symbol.symbolic_compute(Broadcast(()), [left_symbol, constant(0)])
            symbol.name=None
            return True
        else:
            return False


class TemplateDivide(Template):
    from trik.sheng.op import Div
    active_operator = Div

    def simplify(self, symbol: V):
        from trik.sheng.op import SliceAssign
        left_symbol, right_symbol = symbol.input
        if right_symbol.is_constant() and self.value_equal(right_symbol.value, 1):
            self.reduce_symbol(symbol, 0)
            return True
        elif left_symbol.is_constant() and self.value_equal(left_symbol.value, 0):
            symbol.clear_operator()
            symbol.symbolic_compute(SliceAssign(slice(None)), [left_symbol, constant(0)])
            symbol.name=None
            return True
        elif self.symbol_equal(left_symbol, right_symbol):
            symbol.clear_operator()
            symbol.symbolic_compute(SliceAssign(slice(None)), [left_symbol, constant(1)])
            symbol.name=None
            return True
        else:
            return False


class TemplateMultiply(Template):
    from trik.sheng.op import Mul
    active_operator = Mul

    def simplify(self, symbol: V):
        from trik.sheng.op import Pow,Broadcast
        left_symbol, right_symbol = symbol.input
        if left_symbol.is_constant() and self.value_equal(left_symbol.value, 1):
            self.reduce_symbol(symbol, 1)
            return True
        elif right_symbol.is_constant() and self.value_equal(right_symbol.value, 1):
            self.reduce_symbol(symbol, 0)
            return True
        elif (left_symbol.is_constant() and self.value_equal(left_symbol.value, 0)) or(right_symbol.is_constant() and self.value_equal(right_symbol.value, 0)) :
            symbol.clear_operator()
            symbol.symbolic_compute(Broadcast(()),[constant(0)])
            symbol.name=None
            return True
        elif self.symbol_equal(left_symbol, right_symbol):
            symbol.clear_operator()
            symbol.symbolic_compute(Pow(), [left_symbol, constant(2)])
            symbol.name=None
            return True
        elif left_symbol.operator!=None: 
            if left_symbol.operator.operator_sign=='/' and left_symbol.input[0].is_constant() and self.symbol_equal(left_symbol.input[1],right_symbol):
                if left_symbol.input[0].value==1:
                    symbol.clear_operator()
                    symbol.symbolic_compute(Broadcast(()),[constant(1)])
                    symbol.name=None
                    return True
        elif right_symbol.operator!=None: 
            if right_symbol.operator.operator_sign=='/' and right_symbol.input[0].is_constant() and self.symbol_equal(right_symbol.input[1],left_symbol):
                if right_symbol.input[0].value==1:
                    symbol.clear_operator()
                    symbol.symbolic_compute(Broadcast(()),[constant(1)])
                    symbol.name=None
                    return True
        else:
            return False


class TemplatePower(Template):
    from trik.sheng.op import Pow
    active_operator = Pow
    def simplify(self, symbol: V):
        from trik.sheng.op import Broadcast
        left_symbol, right_symbol = symbol.input
        if (self.value_equal(left_symbol.value, 1) and left_symbol.is_constant()) or (self.value_equal(right_symbol.value, 1) and right_symbol.is_constant()):
            self.reduce_symbol(symbol, 0)
            return True
        elif self.value_equal(right_symbol.value, 0) and right_symbol.is_constant():
            symbol.clear_operator()
            symbol.symbolic_compute(Broadcast(()),[constant(1)])    
            symbol.name=None
            return True
        else:
            return False

class TemplateMM(Template):#待优化
    active_operator = MM
    maxlen=4;
    def simplify(self, symbol:V):
        ls=g(symbol)
        if len(ls)>self.maxlen:
            self.maxlen=len(ls)
#             print(ls)
            symbol2=rebuildChain(ls)            
            symbol.clear_operator()
            symbol.symbolic_compute(SliceSelect(slice(None,None,None)),[symbol2])    
            symbol.name=None
            return False


def chainTrace(i,j,s):
    if i==j:
        return []
    ls=[]
    ls+=(chainTrace(i,s[(i,j)],s))
    ls+=(chainTrace(s[(i,j)]+1,j,s))
    ls.append(s[(i,j)])
    return ls    
def matChain(p:list):
    n=len(p)-1
    m,s={},{}
    for i in range(1,n+1):m[(i,i)]=0
    for r in range(2,n+1):
        for i in range(1,n-r+2):
            j=i+r-1
            m[(i,j)]=m[(i+1,j)]+p[i-1]*p[i]*p[j]
            s[(i,j)]=i;
            for k in range(i+1,j):
                t=m[(i,k)]+m[(k+1,j)]+p[i-1]*p[k]*p[j]
                if t<m[(i,j)]:
                    m[(i,j)]=t;s[(i,j)]=k    
    return chainTrace(1, n, s)
def rebuildChain(ls):
    if len(ls)<3:return
    ls1=[ls[0].shape[0]]+[i.shape[1] for i in ls]
    m=matChain(ls1)
    nls=ls[m[0]-1](MM(),ls[m[0]])
    ls[m[0]-1]=nls
    ls[m[0]]=None
    for i in m[1:]:
        j=0
        k=1
        while ls[i+j]==None:j+=1
        while ls[i-k]==None:k+=1
        nls=ls[i-k](MM(),ls[i+j])
        ls[i-k]=nls
        ls[i+j]=None
    return nls

def g(l):#待优化
    if l.operator==None or l.operator.operator_sign!='@':
        return [l]
    ls =[]
    for i in range(l.operator.inputs_count):
        ls+=g(l.input[i])
    return ls

default_templates = [
    TemplateConstant,
    TemplatePlus,
    TemplateSubtract,
    TemplateMultiply,
    TemplateDivide,
    TemplatePower,
    TemplateMM,
]
simp=Simplification(default_templates)