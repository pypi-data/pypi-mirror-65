from ..sheng import V,Pow,Mul,ReduceSum,Abs


class RegularizationLayer:
    def regularization_term(self, *args, **kwargs):
        pass


class RegularizationL1(RegularizationLayer):
    @staticmethod
    def regularization_term(target_symbol: V, decay: float):
        return target_symbol(Abs())(ReduceSum())(Mul(),decay)


class RegularizationL2(RegularizationLayer):
    @staticmethod
    def regularization_term(target_symbol: V, decay: float):
        return target_symbol(Pow(),2)(ReduceSum())(Pow(),0.5)(Mul(),decay)


regularization_l1 = RegularizationL1.regularization_term
regularization_l2 = RegularizationL2.regularization_term


regularization_map = {
    'l1': RegularizationL1,
    'l2': RegularizationL2,
}


def register_regularization(name: str, regularization: RegularizationLayer):
    regularization_map[name.lower()] = regularization


class Regularization:
    def __init__(self, name: str, *args, **kwargs):
        self.__name = name.lower()
        self.__regularization = None
        if self.__name in regularization_map:
            self.__regularization = regularization_map[self.__name](*args, **kwargs)
        else:
            raise ValueError('No such regularization: {}'.format(name))

    def regularization_layer(self):
        return self.__regularization
