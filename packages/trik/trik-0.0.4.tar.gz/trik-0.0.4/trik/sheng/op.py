from functools import reduce
from .tensor import as_symbols,V,constant
from .interface import Operator,numpy, \
    element_wise_shape,matrix_multiply_shape,reduce_shape,transpose_shape,concatenate_shape, \
    slice_shape, rotate90_shape

class Neg(Operator):
    def __init__(self):
        self.operator_sign = '-'
        self.inputs_count = 1

    def f(self, value_a):
        return -value_a

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Neg())]

    def shape(self, shape_a):
        return shape_a, ()


class Abs(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.absolute(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),0), 1, -1])))]

    def shape(self, shape_a):
        return shape_a, ()


class Plus(Operator):
    def __init__(self):
        self.operator_sign = '+'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return value_a + value_b

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1),
                lambda: forward(Mul(),1)]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Sub(Operator):
    def __init__(self):
        self.operator_sign = '-'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return value_a - value_b

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1),
                lambda: forward(Mul(),-1)]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Mul(Operator):
    def __init__(self):
        self.operator_sign = '*'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return value_a * value_b

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_b),
                lambda: forward(Mul(),symbol_a)]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Div(Operator):
    def __init__(self):
        self.operator_sign = '/'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return value_a / value_b

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),symbol_b),
                lambda: forward(Mul(),-1)(Mul(),symbol_a)(Div(),symbol_b(Pow(),2))]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class MM(Operator):
    def __init__(self):
        self.operator_sign = '@'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        if len(value_a.shape) == 0 or len(value_b.shape) == 0:
            return value_a * value_b
        else:
            return value_a @ value_b

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        shape_a = engine.shape2(symbol_a)
        shape_b = engine.shape2(symbol_b)
        if len(shape_a) >= 2:
            axes_a = tuple(range(len(shape_a) - 2)) + (-1, -2)
        else:
            axes_a = None
        if len(shape_b) >= 2:
            axes_b = tuple(range(len(shape_b) - 2)) + (-1, -2)
        else:
            axes_b = None
        return [lambda: forward(MM(),symbol_b(T(axes=axes_a))),
                lambda: symbol_a(T(axes=axes_b))(MM(),forward)]

    def shape(self, shape_a, shape_b):
        return matrix_multiply_shape(shape_a, shape_b)


class T(Operator):
    def __init__(self, axes=None):
        self.inputs_count = 1
        self.arguments = {'axes': axes}

    def f(self, value_a):
        return numpy.transpose(value_a, axes=self.arguments['axes'])

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(T(axes=self.arguments['axes']))]

    def shape(self, shape_a):
        return transpose_shape(shape_a, self.arguments['axes'])


class ReduceSum(Operator):
    def __init__(self, axis: int=None, invariant: bool=False):
        self.inputs_count = 1
        self.arguments = {'axis': axis, 'invariant': invariant}

    def f(self, value_a):
        return numpy.sum(value_a, axis=self.arguments['axis'], keepdims=self.arguments['invariant'])

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        shape_a = engine.shape2(symbol_a)
        axis = self.arguments['axis']
        if axis:
            return [lambda: forward(Expand(axis))(Broadcast(shape_a))]
        else:
            return [lambda: forward(Broadcast(shape_a))]

    def shape(self, shape_a):
        return reduce_shape(shape_a, **self.arguments)


class ReduceMean(Operator):
    def __init__(self, axis: int=None, invariant: bool=False):
        self.inputs_count = 1
        self.arguments = {'axis': axis, 'invariant': invariant}

    def f(self, value_a):
        return numpy.mean(value_a, axis=self.arguments['axis'], keepdims=self.arguments['invariant'])

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        shape_a = engine.shape2(symbol_a)
        axis = self.arguments['axis']
        if axis:
            return [lambda: forward(Expand(axis))(Broadcast(shape_a))(Div(),shape_a[axis])]
        else:
            return [lambda: forward(Broadcast(shape_a))( Div(),reduce(lambda x, y: x * y, shape_a, 1))]

    def shape(self, shape_a):
        return reduce_shape(shape_a, **self.arguments)


class Expand(Operator):
    def __init__(self, axis: int):
        self.inputs_count = 1
        self.arguments = {'axis': axis}

    def f(self, value_a):
        return numpy.expand_dims(value_a, **self.arguments)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(ReduceMean(**self.arguments))]

    def shape(self, shape_a):
        new_shape = list(shape_a)
        new_shape.insert(self.arguments['axis'], 1)
        broadcast_a = [0] * len(shape_a)
        broadcast_a.insert(self.arguments['axis'], 1)
        return tuple(new_shape), tuple(broadcast_a)


class Broadcast(Operator):
    def __init__(self, shape):
        self.inputs_count = 1
        self.arguments = {'shape': shape}

    def f(self, value_a):
        if len(value_a.shape) == 1 and len(self.arguments['shape']) > 1:
            if value_a.shape[0] == self.arguments['shape'][0]:
                value_a = value_a.reshape((value_a.shape[0], 1))
        return numpy.broadcast_to(value_a, **self.arguments)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward]

    def shape(self, shape_a):
        return element_wise_shape(shape_a, self.arguments['shape'])[:2]


class Pow(Operator):
    def __init__(self):
        self.operator_sign = '**'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.power(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_b)(Mul(),symbol_a(Pow(),symbol_b(Sub(),1))),
                lambda: forward(Mul(),symbol_a(Pow(),symbol_b))(Mul(),symbol_a(Log()))]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Log(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.log(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),symbol_a)]

    def shape(self, shape_a):
        return shape_a, ()


class Where(Operator):
    def __init__(self):
        self.inputs_count = 3

    def f(self, value_condition, value_a, value_b):
        return numpy.array(numpy.where(value_condition, value_a, value_b), dtype=float)

    def bprop(self, engine, symbol_forward, symbol_condition, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        
        return [lambda: constant(0),
                lambda: forward(Mul(),V(oprator=Where(),inputs=as_symbols([symbol_condition, forward, 0]))),
                lambda: forward(Mul(),V(oprator=Where(),inputs=as_symbols([symbol_condition, 0,forward])))]

    def shape(self, shape_condition, shape_a, shape_b):
        return element_wise_shape(shape_condition, shape_a, shape_b)


class Eq(Operator):
    def __init__(self):
        self.operator_sign = '=='
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.equal(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: V(operator=Where(),inputs=as_symbols([symbol_a(Eq(),symbol_b), forward, 0])),
                lambda: V(operator=Where(),inputs=as_symbols([symbol_a(Eq(),symbol_b), forward, 0]))]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class NEq(Operator):
    def __init__(self):
        self.operator_sign = '!='
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.not_equal(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(NEq(),symbol_b), forward,0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(NEq(),symbol_b), forward,0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Lt(Operator):
    def __init__(self):
        self.operator_sign = '<'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.less(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class LEq(Operator):
    def __init__(self):
        self.operator_sign = '<='
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.less_equal(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(LEq(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(LEq(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Gt(Operator):
    def __init__(self):
        self.operator_sign = '>'
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.greater(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class GEq(Operator):
    def __init__(self):
        self.operator_sign = '>='
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.greater_equal(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(GEq(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(GEq(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Max(Operator):
    def __init__(self):
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.maximum(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Min(Operator):
    def __init__(self):
        self.inputs_count = 2

    def f(self, value_a, value_b):
        return numpy.minimum(value_a, value_b)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Lt(),symbol_b), forward, 0])),
                lambda:V(operator=Where(),inputs=as_symbols([symbol_a(Gt(),symbol_b), forward, 0])),]

    def shape(self, shape_a, shape_b):
        return element_wise_shape(shape_a, shape_b)


class Sin(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.sin(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_a(Cos()))]

    def shape(self, shape_a):
        return shape_a, ()


class Cos(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.cos(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_a(Sin())(Neg()))]

    def shape(self, shape_a):
        return shape_a, ()


class Tan(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.tan(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),symbol_a(Cos())(Pow(),2))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcSin(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arcsin(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),constant(1)(Sub(),symbol_a(Pow(),2))(Pow(),0.5))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcCos(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arccos(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),-1)(Div(),constant(1)(Sub(),symbol_a(Pow(),constant(2)))(Pow(),0.5))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcTan(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arctan(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),constant(1)(Plus(),symbol_a(Pow(),2)))]

    def shape(self, shape_a):
        return shape_a, ()


class Sinh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.sinh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_a(Cosh()))]

    def shape(self, shape_a):
        return shape_a, ()


class Cosh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.cosh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_a(Sinh()))]

    def shape(self, shape_a):
        return shape_a, ()


class Tanh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.tanh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),constant(1)(Sub(),symbol_a(Tanh())(Pow(),2)))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcSinh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arcsinh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),symbol_a(Pow(),2)(Plus(),1)(Pow(),0.5))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcCosh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arccosh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),symbol_a(Pow(),2)(Sub(),1)(Pow(),0.5))]

    def shape(self, shape_a):
        return shape_a, ()


class ArcTanh(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.arctanh(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),1)(Div(),constant(1)(Sub(),symbol_a(Pow(),2)))]

    def shape(self, shape_a):
        return shape_a, ()


class Exp(Operator):
    def __init__(self):
        self.inputs_count = 1

    def f(self, value_a):
        return numpy.exp(value_a)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Mul(),symbol_a(Exp()))]

    def shape(self, shape_a):
        return shape_a, ()


class SliceAssign(Operator):
    def __init__(self, slice_tuple):
        self.inputs_count = 2
        self.arguments = {'slice_tuple': slice_tuple}

    def f(self, value_a, value_b):
        value_a[self.arguments['slice_tuple']] = value_b
        return value_a

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        slice_tuple = self.arguments['slice_tuple']
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(SliceAssign(slice_tuple),numpy.zeros(engine.shape2(symbol_b))),
                lambda: forward[slice_tuple]]

    def shape(self, shape_a, shape_b):
        shape_select = slice_shape(shape_a, self.arguments['slice_tuple'])[0]
        shape_package = element_wise_shape(shape_select, shape_b)
        if shape_package[0] != shape_select:
            raise ValueError('Can not assign: {} to {} with {}'.format(shape_b, shape_a, self.arguments['slice_tuple']))
        return shape_a, (), shape_package[2]


class SliceSelect(Operator):
    def __init__(self, slice_tuple):
        self.inputs_count = 1
        self.arguments = {'slice_tuple': slice_tuple}

    def f(self, value_a):
        return value_a[self.arguments['slice_tuple']]

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        symbol_zero = constant(numpy.zeros(engine.shape2(symbol_a)))
        return [lambda: symbol_zero(SliceAssign(forward), self.arguments['slice_tuple'])]

    def shape(self, shape_a):
        return slice_shape(shape_a, self.arguments['slice_tuple'])


class Concatenate(Operator):
    def __init__(self, axis: int=0):
        self.inputs_count = 2
        self.arguments = {'axis': axis}

    def f(self, value_a, value_b):
        return numpy.concatenate((value_a, value_b), **self.arguments)

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        split_dimension = engine.shape2(symbol_a)[self.arguments['axis']]
        total_dimension = engine.shape2(symbol_forward)[self.arguments['axis']]
        return [lambda: forward[[slice(None)] * self.arguments['axis'] + [slice(0, split_dimension)]],
                lambda: forward[[slice(None)] * self.arguments['axis'] + [slice(split_dimension, total_dimension)]]]

    def shape(self, *shapes):
        return concatenate_shape(self.arguments['axis'], *shapes)


class Rotate90(Operator):
    def __init__(self, count: int=1, axes: tuple=None):
        self.inputs_count = 1
        self.arguments = {'count': count, 'axes': axes}

    def f(self, value_a):
        return numpy.rot90(value_a, k=self.arguments['count'], axes=self.arguments['axes'])

    def bprop(self, engine, symbol_forward, symbol_a, symbol_b):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Rotate90(-self.arguments['count'] & 3, self.arguments['axes']))]

    def shape(self, shape_a):
        return rotate90_shape(shape_a, **self.arguments)


class Flip(Operator):
    def __init__(self, axis: int):
        self.inputs_count = 1
        self.arguments = {'axis': axis}

    def f(self, value_a):
        return numpy.flip(value_a, self.arguments['axis'])

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Flip(self.arguments['axis']))]

    def shape(self, shape_a):
        return shape_a, ()


class Reshape(Operator):
    def __init__(self, shape):
        self.inputs_count = 1
        self.arguments = {'shape': shape}

    def f(self, value_a):
        return numpy.reshape(value_a, self.arguments['shape'])

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Reshape(engine.shape2(symbol_a)))]

    def shape(self, shape_a):
        return self.arguments['shape'], ()


class Spread(Operator):
    def __init__(self, position):
        self.inputs_count = 1
        self.arguments = {'position': position}

    def f(self, value_a):
        shape_a = value_a.shape
        spread_dimension = numpy.prod(shape_a[self.arguments['position']:])#reduce(lambda a, b: a * b, shape_a[self.arguments['position']:])
        new_shape = shape_a[:self.arguments['position']] + (spread_dimension,)
        return numpy.reshape(value_a, new_shape)

    def bprop(self, engine, symbol_forward, symbol_a):
        forward = engine.bprop(symbol_forward)
        return [lambda: forward(Reshape(engine.shape2(symbol_a)))]

    def shape(self, shape_a):
        spread_dimension = reduce(lambda a, b: a * b, shape_a[self.arguments['position']:])
        new_shape = shape_a[:self.arguments['position']] + (spread_dimension,)
        return new_shape, ()


# def negative(a):
#     return V(operator=Neg(), inputs=as_symbols([a]))
#  
#  
# def absolute(a):
#     return V(operator=Abs(), inputs=as_symbols([a]))
#  
#  
# def plus(a, b):
#     return V(operator=Plus(), inputs=as_symbols([a, b]))
#  
#  
# def subtract(a, b):
#     return V(operator=Sub(), inputs=as_symbols([a, b]))
#  
#  
# def multiply(a, b):
#     return V(operator=Mul(), inputs=as_symbols([a, b]))
#  
#  
# def divide(a, b):
#     return V(operator=Div(), inputs=as_symbols([a, b]))
#  
#  
# def matrix_multiply(a, b):
#     return V(operator=MM(), inputs=as_symbols([a, b]))
#  
#  
# def power(a, b):
#     return V(operator=Pow(), inputs=as_symbols([a, b]))
#  
#  
# def log(a):
#     return V(operator=Log(), inputs=as_symbols([a]))
#  
#  
# def transpose(a, axes: tuple=None):
#     return V(operator=T(axes), inputs=as_symbols([a]))
#  
#  
# def reduce_sum(a, axis: int=None, invariant=False):
#     return V(operator=ReduceSum(axis, invariant), inputs=as_symbols([a]))
#  
#  
# def reduce_mean(a, axis: int=None, invariant=False):
#     return V(operator=ReduceMean(axis, invariant), inputs=as_symbols([a]))
#  
#  
# def expand(a, axis: int):
#     return V(operator=Expand(axis), inputs=as_symbols([a]))
#  
#  
# def broadcast(a, shape):
#     return V(operator=Broadcast(shape), inputs=as_symbols([a]))
#  
#  
# def where(condition, a, b):
#     return V(operator=Where(), inputs=as_symbols([condition, a, b]))
#  
#  
# def equal(a, b):
#     return V(operator=Eq(), inputs=as_symbols([a, b]))
#  
#  
# def not_equal(a, b):
#     return V(operator=NEq(), inputs=as_symbols([a, b]))
#  
#  
# def less(a, b):
#     return V(operator=Lt(), inputs=as_symbols([a, b]))
#  
#  
# def less_equal(a, b):
#     return V(operator=LEq(), inputs=as_symbols([a, b]))
#  
#  
# def greater(a, b):
#     return V(operator=Gt(), inputs=as_symbols([a, b]))
#  
#  
# def greater_equal(a, b):
#     return V(operator=GEq(), inputs=as_symbols([a, b]))
#  
#  
# def maximum(a, b):
#     return V(operator=Max(), inputs=as_symbols([a, b]))
#  
#  
# def minimum(a, b):
#     return V(operator=Min(), inputs=as_symbols([a, b]))
#  
#  
# def sin(a):
#     return V(operator=Sin(), inputs=as_symbols([a]))
#  
#  
# def cos(a):
#     return V(operator=Cos(), inputs=as_symbols([a]))
#  
#  
# def tan(a):
#     return V(operator=Tan(), inputs=as_symbols([a]))
#  
#  
# def arcsin(a):
#     return V(operator=ArcSin(), inputs=as_symbols([a]))
#  
#  
# def arccos(a):
#     return V(operator=ArcCos(), inputs=as_symbols([a]))
#  
#  
# def arctan(a):
#     return V(operator=ArcTan(), inputs=as_symbols([a]))
#  
#  
# def sinh(a):
#     return V(operator=Sinh(), inputs=as_symbols([a]))
#  
#  
# def cosh(a):
#     return V(operator=Cosh(), inputs=as_symbols([a]))
#  
#  
# def tanh(a):
#     return V(operator=Tanh(), inputs=as_symbols([a]))
#  
#  
# def arcsinh(a):
#     return V(operator=ArcSinh(), inputs=as_symbols([a]))
#  
#  
# def arccosh(a):
#     return V(operator=ArcCosh(), inputs=as_symbols([a]))
#  
#  
# def arctanh(a):
#     return V(operator=ArcTanh(), inputs=as_symbols([a]))
#  
#  
# def exp(a):
#     return V(operator=Exp(), inputs=as_symbols([a]))
#  
#  
# def slice_assign(a, b, slice_tuple):
#     return V(operator=SliceAssign(slice_tuple), inputs=as_symbols([a, b]))
#  
#  
# def assign(a, b):
#     return slice_assign(a, b, slice(None))
#  
#  
# def slice_select(a, slice_tuple):
#     return V(operator=SliceSelect(slice_tuple), inputs=as_symbols([a]))
#  
#  
# def concatenate(a, b):
#     return V(operator=Concatenate(), inputs=as_symbols([a, b]))
#  
#  
# def rotate90(a, count, axes):
#     return V(operator=Rotate90(count, axes), inputs=as_symbols([a]))
#  
#  
# def flip(a, axis):
#     return V(operator=Flip(axis), inputs=as_symbols([a]))
#  
# def reshape(a, shape):
#     return V(operator=Reshape(shape), inputs=as_symbols([a]))
#  
#  
# def spread(a, position):
#     return V(operator=Spread(position), inputs=as_symbols([a]))
def where(a,b,c):
    return V(operator=Where(),inputs=as_symbols([a,b,c]))