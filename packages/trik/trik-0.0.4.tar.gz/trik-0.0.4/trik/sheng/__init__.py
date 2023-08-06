from .interface import *
from .tensor import V, \
    variable,constant,placeholder, \
    as_symbol,as_symbols,slice_assign,slice_select
from .optim import *
from .op import *
from .conv import *