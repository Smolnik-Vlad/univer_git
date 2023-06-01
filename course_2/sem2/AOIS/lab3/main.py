import random

from carno_method import carnaugh_method
from mc_clusky_method import McCluskyMethod
from rasch_method import minimizetion_by_rasch_method

table = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
operations_priority = {'!': 6, '*': 5, '+': 4, '~': 3, '->': 2, }


# main_prev()


carnaugh_formula = '(!((x1+x2)*x3))'


def main_funct():
    a = McCluskyMethod()
    c = a.get_sdnf_answer([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']])
    print('sDNF:', c)
    d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    print('sKNF: ', d)
    print('________________________________________________________________')
    print('rasch_method')
    minimizetion_by_rasch_method([['!x1', '!x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', 'x2', 'x3'], ['x1', 'x2', '!x3']],
                                 [['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    # print('sDNF:', c)
    # d = a.get_sknf_answer([['x1', 'x2', 'x3'], ['!x1', 'x2', 'x3'], ['!x1', 'x2', '!x3'], ['!x1', '!x2', '!x3']])
    # print('sKNF: ', d)
    print('________________________________________________________________')
    print('carnaugh_method')
    carnaugh_method(formula=carnaugh_formula)




if __name__ == '__main__':
    main_funct()
