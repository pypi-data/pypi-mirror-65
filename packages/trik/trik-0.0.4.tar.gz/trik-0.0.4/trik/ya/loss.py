from ..sheng import V,Exp,Mul,Neg,Plus,Log,ReduceSum,ReduceMean,Div,Eq,where,Max,Pow,Sub,constant
from ..yu import generate_label_matrix


class LossCategory:
    classification = 0
    regression = 1


class LossLayer:
    loss_type = None

    def loss_function(self, *args, **kwargs):
        raise ValueError("this is abstract")

    
class SoftMaxLoss(LossLayer):
    loss_type = LossCategory.classification

    @staticmethod
    def loss_function(input_symbol: V, label_symbol: V):
        exp_symbol = input_symbol(Exp())
        softmax_value = label_symbol(Mul(),exp_symbol)(ReduceSum(axis=1))(Div(),exp_symbol(ReduceSum(axis=1)))
        loss = softmax_value(Log())(Neg())(ReduceMean())
        return loss


class SVMLoss(LossLayer):
    loss_type = LossCategory.classification

    @staticmethod
    def loss_function(input_symbol: V, label_symbol: V):
        dimension = label_symbol.shape[1]
        label_symbol = label_symbol(Mul(),-(dimension - 1))
        label_symbol = where(label_symbol(Eq(), 0), 1, label_symbol)
        loss = label_symbol(Mul(),input_symbol)(ReduceSum(axis=1))(Plus(),(dimension - 1))(Max(), 0)(ReduceMean())
        return loss


class MSELoss(LossLayer):
    loss_type = LossCategory.regression

    @staticmethod
    def loss_function(input_symbol: V, target_symbol: V):
        loss = input_symbol(Sub(),target_symbol)(Pow(),2)(ReduceMean())
        return loss


softmax_loss = SoftMaxLoss.loss_function
svm_loss = SVMLoss.loss_function
mse_loss = MSELoss.loss_function


def softmax_loss_with_label(input_symbol: V, classification):
    label_symbol = constant(generate_label_matrix(classification)[0])
    return softmax_loss(input_symbol, label_symbol)


def svm_loss_with_label(input_symbol: V, classification):
    label_symbol = constant(generate_label_matrix(classification)[0])
    return svm_loss(input_symbol, label_symbol)


loss_map = {
    'softmax': SoftMaxLoss,
    'svm': SVMLoss,
    'mse': MSELoss,
}


def register_loss(name: str, loss: LossLayer):
    loss_map[name.lower()] = loss


class Loss:
    def __init__(self, name: str, *args, **kwargs):
        self.__name = name.lower()
        self.__loss = None
        if self.__name in loss_map:
            self.__loss = loss_map[self.__name](*args, **kwargs)
        else:
            raise ValueError('No such loss: {}'.format(name))

    def loss_layer(self):
        return self.__loss
