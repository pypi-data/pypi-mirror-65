from .interface import Operator,VCategory,numpy
class V:
    def __init__(self, value=None, shape: tuple=None, name: str=None, operator=None, inputs=None, category: VCategory=None):
        self.__name = None
        self.__input = []
        self.__operator = None
        self.__output = []
        self.__value = None
        self.__shape = None
        self.__scalar = False
        self.__category = None
        # for engin
        self.__variables = set()
        self.__grad_table = {}
        self.__shape2 = {}
        self.__broadcast = {}
        self.__bind ={}
        self.__value_cache = {}
        if isinstance(value, V):
            self.__set_name(value.name)
            self.__set_value(value.value)
            self.__set_shape(value.shape)
            for _input in value.input:
                self.__add_input(_input.clone())
            self.__set_operator(value.__operator)
            for _output in value.output:
                self.__add_output(_output.clone())
            self.__set_category(value.category)
        else:
            self.symbolic_compute(operator, inputs)
            self.__set_value(value)
            self.__set_category(category)
            self.__set_shape(shape)
            self.__set_name(name)
    def __call__(self,op,*arg):
        arg=[self,]+list(arg)
        res=V(operator=op,inputs=as_symbols(arg))
        simp.simplify(res)
        return res
    def __repr__(self):
        if self.__operator is None:
            return self.__name
        else:
            if self.__operator.operator_sign is None:
                arguments = list(map(str, self.input))
                arguments += ['{}={}'.format(k, '\'' + v + '\'' if isinstance(v, str) else v) for k, v in self.__operator.arguments.items()]
                return '{}({})'.format(self.__operator.__class__.__name__, ', '.join(arguments))
            else:
                if len(self.input) < 2:
                    return '{}{}'.format(self.__operator.operator_sign, self.input[0])
                else:
                    return '({} {} {})'.format(self.input[0], self.__operator.operator_sign, self.input[1])

    def __get_name(self):
        return self.__name

    def __set_name(self, name: str):
        if name is None:
            if self.__value is None:
                self.__name = self.__class__.__name__
            else:
                if self.is_scalar():
                    self.__name = str(self.__value)
                else:
                    self.__name = '{}{}'.format(self.__class__.__name__, self.__value.shape)
        else:
            self.__name = name

    name = property(__get_name, __set_name)

    def __get_category(self):
        return self.__category

    def __set_category(self, category: VCategory):
        if category is None:
            if self.__category is None:
                self.__category = VCategory.variable
        else:
            if self.__category == VCategory.operator:
                if category != VCategory.operator:
                    raise ValueError('Can not change category of Operator V.')
            if category == VCategory.variable:
                self.__category = category
            elif category == VCategory.constant:
                self.__category = category
                if self.__value is None:
                    raise ValueError('constant V must have value.')
            elif category == VCategory.placeholder:
                self.__category = category
                if self.__value is not None:
                    self.__set_shape(self.__value.shape)
            elif category == VCategory.operator:
                if self.operator is not None:
                    self.__category = category
                else:
                    raise ValueError('Can not convert other V to Operator V.')
            else:
                raise ValueError('Invalid category: {}'.format(category))

    category = property(__get_category, __set_category)

    def __get_value(self):
        return self.__value

    def __set_value(self, tensor):
        if tensor is not None:
            if self.__category == VCategory.constant:
                raise ValueError('Can not change value for constant.')
            else:
                if self.__operator is None:
                    self.__value = numpy.array(tensor, dtype=float)
                    self.__scalar = len(self.value.shape) == 0
                    self.__set_category(VCategory.variable)
                else:
                    raise ValueError('Can not assign value for Operator V.')

    value = property(__get_value, __set_value)

    def __get_shape(self):
        if self.__category == VCategory.placeholder:
            return self.__shape
        else:
            if self.__operator is None:
                return self.__value.shape
            else:
                return self.shape2(self)
#                 raise ValueError('Operator V has no shape.')

    def __set_shape(self, shape: tuple):
        if shape is not None:
            if self.__category == VCategory.placeholder:
                self.__shape = shape
            else:
                raise ValueError('Only Placeholder can set shape.')

    shape = property(__get_shape, __set_shape)

    def __get_operator(self):
        return self.__operator

    def __set_operator(self, operator):
        if operator is not None:
            if isinstance(operator, Operator):
                self.__operator = operator
            else:
                raise ValueError('Operator must be Operator.')

    operator = property(__get_operator, __set_operator)

    def __get_input(self):
        return self.__input

    input = property(__get_input)

    def __add_input(self, symbol):
        if isinstance(symbol, V):
            self.__input.append(symbol)
        else:
            raise ValueError('Input must be V.')

    def __get_output(self):
        return self.__output

    output = property(__get_output)

    def __add_output(self, symbol):
        if isinstance(symbol, V):
            self.__output.append(symbol)
        else:
            raise ValueError('Output must be V.')

    def symbolic_compute(self, operator, inputs):
        if operator is not None and inputs:
            self.__set_operator(operator)
            inputs_count = operator.inputs_count
            if inputs_count is None:
                inputs_count = len(inputs)
            self.__input = []
            self.__scalar = True
            for symbol in inputs[:inputs_count]:
                if isinstance(symbol, V):
                    if not symbol.is_scalar():
                        self.__scalar = False
                    self.__add_input(symbol)
                    symbol.__add_output(self)
                else:
                    raise ValueError('Input must be V.')
            self.__set_category(VCategory.operator)

    def remove_input(self, symbol):
        new_input = []
        find_input = None
        for each_input in self.__input:
            if hash(each_input) != hash(symbol):
                new_input.append(each_input)
            else:
                find_input = each_input
        self.__input = new_input
        if find_input is not None:
            find_input.remove_output(self)

    def remove_output(self, symbol):
        new_output = []
        find_output = None
        for each_output in self.__output:
            if hash(each_output) != hash(symbol):
                new_output.append(each_output)
            else:
                find_output = each_output
        self.__output = new_output
        if find_output is not None:
            find_output.remove_input(self)

    def clear_input(self):
        for symbol in set(self.__input):
            symbol.remove_output(self)
        self.__input = []

    def clear_output(self):
        for symbol in set(self.__output):
            symbol.remove_input(self)
        self.__output = []

    def clear_operator(self):
        self.clear_input()
        self.__operator = None
        self.__category = VCategory.variable

    def destroy(self):
        self.clear_input()
        self.clear_output()
        self.__value = None
        self.__operator = None

    def is_scalar(self):
        return self.__scalar
    def is_constant(self):
        return self.__category == VCategory.constant
    def is_variable(self):
        return self.__category == VCategory.variable
    def is_placeholder(self):
        return self.__category == VCategory.placeholder
    def is_operator(self):
        return self.__category == VCategory.operator

    def symbolic_hash(self):
        if self.is_operator():
            inputs_symbolic_hash = [each_input.symbolic_hash() for each_input in self.input]
            return '{}({})'.format(self.operator.__class__.__name__, ','.join(inputs_symbolic_hash))
        else:
            return str(hash(self))

    def __hash__(self):
        return id(self)
    def __getitem__(self, item):
        return slice_select(self, item)
    def __setitem__(self, key, value):
        return slice_assign(self, value, key)
    
    def clear(self):
        self.__grad_table = {}
        self.__shape2 = {}
        self.__broadcast = {}
        self.__value_cache = {}
    def get_variables(self):
        return self.__variables

    def set_variables(self, symbol):
        if symbol is None:
            symbol = set()
            symbol_set ={self} 
            while len(symbol_set):
                any_symbol = symbol_set.pop()
                if any_symbol.is_variable():
                    symbol.add(any_symbol)
                elif any_symbol.is_operator():
                    symbol_set |= set(any_symbol.input)
        old_variables = set(self.__variables)
        if isinstance(symbol, V):
            symbols = {symbol}
        else:
            symbols = set(symbol)
        for symbol in symbols:
            if isinstance(symbol, V) and not symbol.is_operator():
                self.__variables.add(symbol)
            else:
                raise ValueError('Variable must be V.')
        unused_variables = old_variables - self.__variables
        for variable in unused_variables:
            if variable in self.__grad_table:
                del self.__grad_table[variable]

    variables = property(get_variables, set_variables)

    def get_bind(self,):
        return self.__bind

    def set_bind(self,bind_data: dict):
        old_bind = self.__bind
        self.__bind ={}
        need_clear = False
        for s, d in bind_data.items():
            if s.category == VCategory.constant:
                raise ValueError('Can not bind data for constant.')
            d_array = numpy.array(d)
            if s in old_bind:
                if old_bind[s].shape != d_array.shape:
                    need_clear = True
            else:
                need_clear = True
            self.__bind[s] = d_array
        if need_clear:
            self.clear()
    bind=property(get_bind,set_bind)
    def get_value_cache(self):
        return self.__value_cache

    def set_value_cache(self, value_cache: dict):
        self.__value_cache = value_cache

    value_cache = property(get_value_cache, set_value_cache)

    def modified(self):
        self.__value_cache = {}

    def __compute_value(self,symbol):
        if not isinstance(symbol,V):raise ValueError('symbol Must be V')
        if not symbol.is_operator():
            if symbol in self.__bind:
                return numpy.array(self.__bind[symbol])
            else:
                if symbol.value is None or symbol.is_placeholder():
                    raise ValueError('V must bind data: {}'.format(symbol))
                else:
                    return symbol.value
        else:
            if symbol in self.__value_cache:
                return self.__value_cache[symbol]
            else:
                compute_inputs =[self.__compute_value(_s) for _s in symbol.input]
                symbol_value = symbol.operator.f(*compute_inputs)
                self.__value_cache[symbol] =symbol_value
                return symbol_value

    def __build_grad(self, variable):
        if not isinstance(variable,V):
            raise ValueError('variable must be V')
        if hash(self) == hash(variable):
            from trik.sheng.op import Broadcast
            self.__grad_table[variable] = constant(1)(Broadcast(self.shape2(self)))
            return
        current_operator = None
        index = -1
        for forward in variable.output:
            if forward.is_constant():continue
            if self.bprop(forward) is not None:
                if current_operator != forward.operator:
                    current_operator = forward.operator
                    index = -1
                gradients = forward.operator.bprop(self, forward, *forward.input)
                for i, _variable in enumerate(forward.input, start=index + 1):
                    if hash(_variable) == hash(variable):
                        index = i
                        break
                if gradients:current_gradient=gradients[index]()
                else:current_gradient=constant(0)
                if forward.operator.auto_reduce:
                    invariant = 0
                    from trik.sheng.op import ReduceSum
                    for i, d in enumerate(self.broadcast(variable, forward)):
                        if d > 0:
                            current_gradient = current_gradient(ReduceSum(axis=i + invariant, invariant=True))
                        elif d < 0:
                            current_gradient = current_gradient(ReduceSum(axis=i + invariant, invariant=False))
                            invariant -= 1
                if variable not in self.__grad_table:
                    self.__grad_table[variable] = current_gradient
                else:
                    from trik.sheng.op import Plus
                    self.__grad_table[variable] = self.__grad_table[variable](Plus(),current_gradient)
        if variable in self.__grad_table:
            simp.simplify(self.__grad_table[variable])

    def __compute_shape(self, symbol):
        if not isinstance(symbol,V):
            raise ValueError('symbol must be V')
        if not symbol.is_operator():
            if symbol in self.__bind:
                self.__shape2[symbol] = self.__bind[symbol].shape
            else:
                if symbol.shape is None:
                    raise ValueError('Placeholder must bind data or set shape: {}'.format(symbol))
                else:
                    self.__shape2[symbol] = symbol.shape
        else:
            shape_broadcasts = symbol.operator.shape(*[self.shape2(s) for s in symbol.input])
            shape = shape_broadcasts[0]
            broadcasts = shape_broadcasts[1:]
            self.__shape2[symbol] = shape
            for input_symbol, input_broadcast in zip(symbol.input, broadcasts):
                if sum([abs(d) for d in input_broadcast]) > 0:
                    self.__broadcast.setdefault(input_symbol, {})
                    self.__broadcast[input_symbol].setdefault(symbol, {})
                    self.__broadcast[input_symbol][symbol] = input_broadcast

    def val(self):
        return self.__compute_value(self)

    def differentiate(self):
        for variable in self.__variables:
            if variable not in self.__grad_table:
                self.__build_grad(variable)

    def bprop(self, variable):
        if not isinstance(variable,V):
            raise ValueError('variable must be V')
        if variable not in self.__grad_table:
            self.__build_grad(variable)
        return self.__grad_table.get(variable, None)

    def shape2(self, variable):
        if not isinstance(variable,V):
            raise ValueError('variable must be V')
        if variable not in self.__shape2:
            self.__compute_shape(variable)
        return self.__shape2.get(variable, None)

    def broadcast(self, from_variable, to_variable):
        if not isinstance(from_variable,V) or not isinstance(to_variable,V):
            raise ValueError('variable must be V')
        if from_variable not in self.__broadcast:
            self.__compute_shape(from_variable)
        if from_variable not in self.__broadcast:
            return ()
        else:
            if to_variable not in self.__broadcast[from_variable]:
                return ()
            else:
                return self.__broadcast[from_variable][to_variable]
    
def constant(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
    return V(value, shape, name, operator, inputs, VCategory.constant)
def variable(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
    return V(value, shape, name, operator, inputs, VCategory.variable)
def placeholder(value=None, shape: tuple=None, name: str=None, operator=None, inputs=None):
    return V(value, shape, name, operator, inputs, VCategory.placeholder)

def as_symbol(thing):
    if isinstance(thing, V):
        return thing
    else:
        return constant(thing)
def as_symbols(things):
    return list(map(as_symbol, things))
def slice_assign(a, b, slice_tuple):
    from trik.sheng.op import SliceAssign
    return V(operator=SliceAssign(slice_tuple), inputs=as_symbols([a, b]))  
def slice_select(a, slice_tuple):
    from trik.sheng.op import SliceSelect
    return V(operator=SliceSelect(slice_tuple), inputs=as_symbols([a]))
from .ab import simp