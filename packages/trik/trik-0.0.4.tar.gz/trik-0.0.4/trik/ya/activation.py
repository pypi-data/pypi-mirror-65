from ..sheng import V, ReduceSum,Plus,Div,Max,Exp,Tanh,Neg,constant,Log,Abs
from ..yu import xavier_initialization, he_initialization, bias_initialization


class ActivationLayer:
    def activation_layer(self):
        return self

    def activation_function(self, *args, **kwargs):
        raise ValueError("this is abstract")

    @staticmethod
    def weight_initialization(shape):
        weight = xavier_initialization(shape)
        return weight

    @staticmethod
    def bias_initialization(shape):
        bias = bias_initialization(shape)
        return bias


class RectifiedLinearUnits(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        output_symbol = input_symbol(Max(), 0)
        return output_symbol

    @staticmethod
    def weight_initialization(shape):
        weight = he_initialization(shape)
        return weight


class SoftMax(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        exp_symbol = input_symbol(Exp())
        output_symbol = exp_symbol(Div(),exp_symbol(ReduceSum()))
        return output_symbol


class HyperbolicTangent(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        output_symbol = input_symbol(Tanh())
        return output_symbol


class Sigmoid(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        output_symbol = constant(1)(Div(),input_symbol(Neg())(Exp())(Plus(),1))
        return output_symbol


class SoftPlus(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        output_symbol = input_symbol(Exp())(Plus(),1)(Log())
        return output_symbol


class SoftSign(ActivationLayer):
    @staticmethod
    def activation_function(input_symbol: V):
        output_symbol = input_symbol(Div(),input_symbol(Abs())(Plus(),1))
        return output_symbol


relu = RectifiedLinearUnits.activation_function
softmax = SoftMax.activation_function
sigmoid = Sigmoid.activation_function
softplus = SoftPlus.activation_function
softsign = SoftSign.activation_function


activation_map = {
    'relu': RectifiedLinearUnits,
    'softmax': SoftMax,
    'tanh': HyperbolicTangent,
    'sigmoid': Sigmoid,
    'softplus': SoftPlus,
    'softsign': SoftSign,
}


def register_activation(name: str, activation: ActivationLayer):
    activation_map[name.lower()] = activation


class Activation:
    def __init__(self, name: str, *args, **kwargs):
        self.__name = name.lower()
        self.__activation = None
        if self.__name in activation_map:
            self.__activation = activation_map[self.__name](*args, **kwargs)
        else:
            raise ValueError('No such activation: {}'.format(name))

    def activation_layer(self):
        return self.__activation
