import random

from carno_method import CarnoMethod
from mc_clusky_method import McCluskyMethod
from rasch_method import RaschMethod

table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
operations_priority = {'!': 6, '*': 5, '+': 4, '~': 3, '->': 2, }

# main_prev()


def main_funct():
    a = McCluskyMethod()
    c = a.get_sdnf_answer([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
    print('sDNF:', c)
    d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    print('sKNF: ', d)
    print('________________________________________________________________')
    a = RaschMethod()
    c = a.get_sdnf_answer([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
    print('sDNF:', c)
    d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    print('sKNF: ', d)
    print('________________________________________________________________')
    a = CarnoMethod()
    c = a.get_sdnf_answer([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
    print('sDNF:', c)
    d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    print('sKNF: ', d)


if __name__ == '__main__':
    main_funct()