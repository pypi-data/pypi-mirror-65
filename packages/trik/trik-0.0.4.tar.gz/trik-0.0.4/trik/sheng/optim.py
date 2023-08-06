from .tensor import V,constant
from .interface import Optimizer

class GradientDescentOptimizer(Optimizer):
    def __init__(self, rate: float, consistent: bool=True):
        self.__rate = rate
        self.__consistent = consistent
        self.__gradient_engine=constant(1)
    def __repr__(self):
        return '{}(rate={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__consistent)

    def optimize(self, engine , calculate_function):
        variables = engine.variables
        for variable in variables:
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            if self.__gradient_engine:self.__gradient_engine.bind=engine.bind
            else :self.__gradient_engine=constant(1)
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            variable.value = calculate_function(variable.value, self.__rate * self.__gradient_engine.val())
        engine.modified()
        self.__gradient_engine.modified()


class MomentumOptimizer(Optimizer):
    def __init__(self, rate: float, factor: float=0, consistent: bool=True):
        self.__rate = rate
        self.__factor = factor
        self.__consistent = consistent
        self.__old_gradient_map = {}
        self.__gradient_engine = V()

    def __repr__(self):
        return '{}(rate={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__consistent)

    def optimize(self, engine, calculate_function):
        variables = engine.variables
        for variable in variables:
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            self.__gradient_engine.set_bind(engine.get_bind())
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            momentum = self.__gradient_engine.val() + self.__factor * self.__old_gradient_map.get(variable, 0)
            self.__old_gradient_map[variable] = momentum
            variable.value = calculate_function(variable.value, self.__rate * momentum)
        engine.modified()
        self.__gradient_engine.modified()


class AdaptiveGradientOptimizer(Optimizer):
    def __init__(self, rate: float, consistent: bool=True):
        self.__rate = rate
        self.__consistent = consistent
        self.__gradient_engine = V()
        self.__accumulate_gradient_map = {}

    def __repr__(self):
        return '{}(rate={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__consistent)

    def optimize(self, engine, calculate_function):
        variables = engine.variables
        for variable in variables:
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            self.__gradient_engine.set_bind(engine.get_bind())
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            current_gradient = self.__gradient_engine.val()
            self.__accumulate_gradient_map.setdefault(variable, 0)
            self.__accumulate_gradient_map[variable] += current_gradient ** 2
            regularization_value = current_gradient / (self.__accumulate_gradient_map[variable] + 1e-8) ** 0.5
            variable.value = calculate_function(variable.value, self.__rate * regularization_value)
        engine.modified()
        self.__gradient_engine.modified()


class AdaptiveDeltaOptimizer(Optimizer):
    def __init__(self, decay: float, consistent: bool=True):
        self.__decay = decay
        self.__consistent = consistent
        self.__gradient_engine = V()
        self.__accumulate_gradient_map = {}
        self.__expectation_map = {}

    def __repr__(self):
        return '{}(decay={}, consistent={})'.format(self.__class__.__name__, self.__decay, self.__consistent)

    def optimize(self, engine, calculate_function):
        variables = engine.variables
        for variable in variables:
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            self.__gradient_engine.set_bind(engine.get_bind())
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            current_gradient = self.__gradient_engine.val()
            self.__accumulate_gradient_map.setdefault(variable, 0)
            self.__expectation_map.setdefault(variable, 0)
            self.__accumulate_gradient_map[variable] = self.__decay * self.__accumulate_gradient_map[variable] + (1 - self.__decay) * current_gradient ** 2
            delta = (self.__expectation_map[variable] + 1e-8) ** 0.5 / (self.__accumulate_gradient_map[variable] + 1e-8) ** 0.5 * current_gradient
            self.__expectation_map[variable] = self.__decay * self.__expectation_map[variable] + (1 - self.__decay) * delta ** 2
            variable.value = calculate_function(variable.value, delta)
        engine.modified()
        self.__gradient_engine.modified()


class RootMeanSquarePropOptimizer(Optimizer):
    def __init__(self, rate: float, consistent: bool=True):
        self.__rate = rate
        self.__consistent = consistent
        self.__gradient_engine = V()
        self.__mean_map = {}
        self.__step = 1

    def __repr__(self):
        return '{}(rate={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__consistent)

    def optimize(self, engine, calculate_function):
        variables = engine.variables
        for variable in variables:
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            self.__gradient_engine.set_bind(engine.get_bind())
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            current_gradient = self.__gradient_engine.val()
            self.__mean_map.setdefault(variable, 0)
            self.__mean_map[variable] *= (self.__step - 1) / self.__step
            self.__mean_map[variable] += current_gradient ** 2 / self.__step
            self.__step += 1
            regularization_value = current_gradient / (self.__mean_map[variable] + 1e-8) ** 0.5
            variable.value = calculate_function(variable.value, self.__rate * regularization_value)
        engine.modified()
        self.__gradient_engine.modified()


class AdaptiveMomentEstimationOptimizer(Optimizer):
    def __init__(self, rate: float, decay: float=0.9, square_decay: float=0.999, consistent: bool=True):
        self.__rate = rate
        self.__decay = decay
        self.__square_decay = square_decay
        self.__consistent = consistent
        self.__gradient_engine = V()
        self.__estimation_map = {}
        self.__square_estimation_map = {}
        self.__step = 1

    def __repr__(self):
        return '{}(rate={}, decay={}, square_decay={}, consistent={})'.format(self.__class__.__name__, self.__rate, self.__decay, self.__square_decay, self.__consistent)

    def optimize(self, engine, calculate_function):
        
        variables = engine.variables
        for variable in variables:
            
            value_cache = self.__gradient_engine.value_cache
            self.__gradient_engine = engine.bprop(variable)
            self.__gradient_engine.bind=engine.bind
            if self.__consistent:
                self.__gradient_engine.value_cache = value_cache
            current_gradient = self.__gradient_engine.val()
            self.__estimation_map.setdefault(variable, 0)
            self.__square_estimation_map.setdefault(variable, 0)
            self.__estimation_map[variable] = self.__decay * self.__estimation_map[variable] + (1 - self.__decay) * current_gradient
            self.__square_estimation_map[variable] = self.__square_decay * self.__square_estimation_map[variable] + (1 - self.__square_decay) * current_gradient ** 2
            estimation = self.__estimation_map[variable] / (1 - self.__decay ** self.__step)
            square_estimation = self.__square_estimation_map[variable] / (1 - self.__square_decay ** self.__step)
            self.__step += 1
            regularization_value = estimation / (square_estimation + 1e-8) ** 0.5
            variable.value = calculate_function(variable.value, self.__rate * regularization_value)
        engine.modified()
        self.__gradient_engine.modified()
        
