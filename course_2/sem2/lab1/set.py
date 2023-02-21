from typing import List


class MySet:
    def __init__(self, ):
        self.__elements: List[str] = []
        self.__subsets: List[MySet] = []

    @property
    def subsets(self):
        return self.__subsets

    @property
    def elements(self):
        return self.__elements

    def __from_class_to_set(my_set_class):
        my_set_set = set()
        my_set_set.update(set(my_set_class.elements))
        for subset in my_set_class.subsets:
            my_set_set.add(frozenset(subset.__from_class_to_set()))
        return my_set_set

    @staticmethod
    def __from_set_to_class(my_set_set: set):
        my_set_class = MySet()
        for element in my_set_set:
            if type(element) != frozenset:
                my_set_class.elements.append(element)
            else:
                my_set_class.subsets.append(MySet.__from_set_to_class(element))
        return my_set_class

    def __add__(self, other):  # type: (MySet) -> MySet
        first_set = self.__from_class_to_set()
        second_set = other.__from_class_to_set()
        sum_set = first_set.union(second_set)
        result_set = MySet.__from_set_to_class(sum_set)
        return result_set

    def __mul__(self, other): #type: (MySet) -> MySet
        first_set = self.__from_class_to_set()
        second_set = other.__from_class_to_set()
        compose_set = first_set.intersection(second_set)
        result_set = MySet.__from_set_to_class(compose_set)
        return result_set


    def __sub__ (self, other): #type: (MySet) -> MySet
        first_set = self.__from_class_to_set()
        second_set = other.__from_class_to_set()
        symmetric_difference = first_set.symmetric_difference(second_set)
        result_set = MySet.__from_set_to_class(symmetric_difference)
        return result_set

    def __div__ (self, other): #type: (MySet) -> MySet
        first_set = self.__from_class_to_set()
        second_set = other.__from_class_to_set()
        difference = first_set.difference(second_set)
        print(difference)
        result_set = MySet.__from_set_to_class(difference)
        return result_set


#
# a = MySet()
# a.elements.extend(['a', 'b'])
# a_2 = MySet()
# a_2.elements.extend(['c', 'd'])
# a.subsets.append(a_2)
#
# b = MySet()
# b.elements.extend(['c', 'b'])
# b_2 = MySet()
# b_2.elements.extend(['m', 'd'])
# b.subsets.append(b_2)
#
# c: MySet = a + b
#
# print(f'{c.elements}, {c.subsets[0].elements}, {c.subsets[1].elements}')
# d: MySet = a * b
#
# print(f'{d.elements}')
# # c = a + a
#
# d: MySet = a.__div__(b)
#
