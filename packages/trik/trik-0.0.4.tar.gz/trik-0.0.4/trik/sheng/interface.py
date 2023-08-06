import numpy
def element_wise_shape(*shape_list):
    broadcast_map = {_shape: [] for _shape in shape_list}
    new_shape = []
    for shape in shape_list:#找最大len的shape
        if len(shape) > len(new_shape):
            new_shape = list(shape)
    for i in range(-len(new_shape), 0):
        index = len(new_shape) + i
        dimensions = {}
        for shape in shape_list:
            if -i > len(shape):
                broadcast_map[shape].append(-1)
            else:
                broadcast_map[shape].append(0)
                dimensions[shape] = shape[i]
        new_shape[index] = max([_d for _, _d in dimensions.items()])
        for shape, dimension in dimensions.items():
            if dimension != new_shape[index]:
                if dimension == 1:
                    broadcast_map[shape][-1] = 1
                else:
                    raise ValueError('Can not broadcast these shapes: {}'.format(shape_list))
    return (tuple(new_shape),) + tuple(tuple(broadcast_map[_shape]) for _shape in shape_list)

def matrix_multiply_shape(shape_a, shape_b):
    try:
        if len(shape_a) == 0 or len(shape_b) == 0:
            raise ValueError()
        if len(shape_a) == 1 and len(shape_b) == 1:
            if shape_a[0] == shape_b[0]:
                return (), (), ()
            else:
                raise ValueError()
        if len(shape_a) == 1:
            if shape_a[0] == shape_b[-2]:
                new_shape = list(shape_b)
                del new_shape[-2]
                return tuple(new_shape), (), ()
            else:
                raise ValueError()
        if len(shape_b) == 1:
            if shape_a[-1] == shape_b[0]:
                return shape_a[:-1], (), ()
            else:
                raise ValueError()
        if shape_a[-1] == shape_b[-2]:
            gap = abs(len(shape_a) - len(shape_b))
            if len(shape_a) > len(shape_b):
                if shape_a[gap:-2] != shape_b[:-2]:
                    raise ValueError()
                new_shape = list(shape_a)
                broadcast_a = (0,) * len(shape_a)
                broadcast_b = shape_a[:gap] + (0, 0)
            else:
                if shape_b[gap:-2] != shape_a[:-2]:
                    raise ValueError()
                new_shape = list(shape_b)
                broadcast_a = shape_b[:gap] + (0, 0)
                broadcast_b = (0,) * len(shape_b)
            new_shape[-1] = shape_b[-1]
            new_shape[-2] = shape_a[-2]
            return tuple(new_shape), broadcast_a, broadcast_b
        else:
            raise ValueError()
    except ValueError:
        raise ValueError('Can not execute matrix multiply with these two shapes: a={}, b={}'.format(shape_a, shape_b))


def reduce_shape(shape_a, axis, invariant):
    if axis is None:
        return (), ()
    else:
        new_shape = list(shape_a)
        if invariant:
            new_shape[axis] = 1
        else:
            del new_shape[axis]
        return tuple(new_shape), ()


def transpose_shape(shape_a, axes):
    if axes is None:
        return tuple(reversed(shape_a)), ()
    else:
        if len(set(axes)) == len(axes):
            if set(axes) == set(range(len(axes))) and len(axes) == len(shape_a):
                new_shape = [0] * len(shape_a)
                for i, d in zip(axes, shape_a):
                    new_shape[i] = d
                return tuple(new_shape), ()
            else:
                raise ValueError('Invalid axes for this Shape: shape={}, axes={}'.format(shape_a, axes))
        else:
            raise ValueError('Repeated axis in axes: {}'.format(axes))


def concatenate_shape(axis, *shape_list):
    new_shape = list(shape_list[0])
    shape_len = len(new_shape)
    for shape in shape_list[1:]:
        if len(shape) == len(shape):
            for i in range(shape_len):
                if i == axis:
                    new_shape[i] += shape[i]
                else:
                    if new_shape[i] != shape[i]:
                        raise ValueError('Concatenate shape not match: {}'.format(shape_list))
        else:
            raise ValueError('All shapes must have same dimensions')
    return (tuple(new_shape),) + () * len(shape_list)


def slice_shape(shape_a, slice_list):
    if not isinstance(slice_list, list):
        slice_list = [slice_list]
    new_shape = list(shape_a)
    delete_dimension = 0
    for i, s in enumerate(slice_list):
        index = i - delete_dimension
        if index < len(shape_a):
            if isinstance(s, slice):
                new_shape[index] = len(([0] * shape_a[index])[s])
            elif isinstance(s, int):
                del new_shape[index]
                delete_dimension += 1
            else:
                raise ValueError('Invalid slice type: {}'.format(type(s)))
        else:
            raise ValueError('Shape not match slice: shape={} slice={}'.format(shape_a, slice_list))
    return tuple(new_shape), ()


def rotate90_shape(shape_a, count, axes):
    new_shape = list(shape_a)
    if count % 2 == 0:
        return tuple(new_shape), ()
    else:
        new_shape[axes[0]], new_shape[axes[1]] = new_shape[axes[1]], new_shape[axes[0]]
        return tuple(new_shape), ()

class VCategory:
    variable = 0
    constant = 1
    placeholder = 2
    operator = 3
    
class Operator:
    operator_sign = None
    inputs_count = None
    auto_reduce = True
    arguments = {}

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, ', '.join(['{}={}'.format(key, value) for key, value in self.arguments.items()]))

    def f(self, *args, **kwargs):
        raise ValueError("this is abstract")

    def bprop(self, *args, **kwargs):
        raise ValueError("this is abstract")

    def shape(self, *args, **kwargs):
        raise ValueError("this is abstract")

class Template:
    active_operator = None
    def __init__(self):
        if self.active_operator is None:
            self.active_sign = None
        else:
            self.active_sign = self.active_operator.__name__

    @staticmethod
    def reduce_symbol(symbol, index: int):
        from .tensor import V
        if not isinstance(symbol,V):raise ValueError("symbol Must be V")
        input_list = symbol.input
        reduce_to_symbol = input_list[index]
        symbol.clear_operator()
        symbol.value = reduce_to_symbol.value
        symbol.name = reduce_to_symbol.name
        if reduce_to_symbol.is_operator():
            symbol.symbolic_compute(reduce_to_symbol.operator, reduce_to_symbol.input)
        else:
            symbol.category = reduce_to_symbol.category

    @staticmethod
    def value_equal(a, b):
        result = a == b
        if isinstance(result, bool) or isinstance(result, numpy.bool_):
            return result
        elif isinstance(result, numpy.ndarray):
            return result.all()
        else:
            raise Exception('Never reached.')

    @staticmethod
    def symbol_equal(a, b):
        from .tensor import V
        if not isinstance(a,V) or not isinstance(b,V):raise ValueError("symbol Must be V")
        return a.symbolic_hash() == b.symbolic_hash()

    def simplify(self, symbol):
        raise ValueError("this is abstract")

class Simplification:
    def __init__(self,templates:list):
        self.__templates = {}
        for template in templates:
            self.register(template())
    def operator_trigger(self, operator: Operator):
        operator_sign = operator.__class__.__name__
        if operator_sign in self.__templates:
            return self.__templates[operator_sign]
        else:
            return set()

    def register(self, template: Template):
        active_operator = template.active_sign
        self.__templates.setdefault(active_operator, set())
        self.__templates[active_operator].add(template)

    def simplify(self, symbol):
        from .tensor import V
        if not isinstance(symbol,V):raise ValueError("symbol Must be V")
        while self.simplify_cycle(symbol):
            pass
    def simplify_cycle(self, symbol):
        from .tensor import V
        if not isinstance(symbol,V):raise ValueError("symbol Must be V")
        effective = False
        templates = list(self.operator_trigger(symbol.operator)) + list(self.__templates[None])
        if templates:
            for template in templates:
                if template.simplify(symbol):
                    effective |= True
                    break
        for next_symbol in symbol.input:
            if next_symbol.operator is not None:
                effective |= self.simplify_cycle(next_symbol)
        return effective
    
class Optimizer:
    def optimize(self, engine,calculate_function):
        raise ValueError("this is abstract")
    def minimize(self, engine,steps: int=1):
        for _ in range(steps):
            self.optimize(engine,lambda v, g: v - g)