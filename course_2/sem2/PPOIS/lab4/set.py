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

    def from_class_to_set(my_set_class)->set:
        my_set_set = set()
        my_set_set.update(set(my_set_class.elements))
        for subset in my_set_class.subsets:
            my_set_set.add(frozenset(subset.from_class_to_set()))
        return my_set_set

    def from_class_to_list(my_set_class)->list:
        my_set_list = []
        my_set_list.extend(my_set_class.elements)
        for subset in my_set_class.subsets:
            my_set_list.append(subset.from_class_to_list())
        return my_set_list


    @staticmethod
    def from_set_to_class(my_set_set: set):
        my_set_class = MySet()
        for element in my_set_set:
            if type(element) != frozenset and type(element) != list:
                my_set_class.elements.append(element)
            else:
                my_set_class.subsets.append(MySet.from_set_to_class(element))
        return my_set_class

    def __add__(self, other):  # type: (MySet) -> MySet
        first_set = self.from_class_to_set()
        second_set = other.from_class_to_set()
        sum_set = first_set.union(second_set)
        result_set = MySet.from_set_to_class(sum_set)
        return result_set

    def __mul__(self, other):  # type: (MySet) -> MySet
        first_set = self.from_class_to_set()
        second_set = other.from_class_to_set()
        compose_set = first_set.intersection(second_set)
        result_set = MySet.from_set_to_class(compose_set)
        return result_set

    def __sub__(self, other):  # type: (MySet) -> MySet
        first_set = self.from_class_to_set()
        second_set = other.from_class_to_set()
        symmetric_difference = first_set.symmetric_difference(second_set)
        result_set = MySet.from_set_to_class(symmetric_difference)
        return result_set

    def __truediv__(self, other):  # type: (MySet) -> MySet
        first_set = self.from_class_to_set()
        second_set = other.from_class_to_set()
        difference = first_set.difference(second_set)
        result_set = MySet.from_set_to_class(difference)
        return result_set

    def __getitem__(self, key):

        my_set = self.from_class_to_list()

        if isinstance(slice, int):
            start, stop, step = key.indices(len(self.elements))

            new_set = my_set[start:stop:step]
            return MySet.from_set_to_class(new_set)

        elif isinstance(key, int):
            new_set = my_set[key]
            return MySet.from_set_to_class(new_set)

        else:
            raise TypeError(f"Unsupported type {type(key)}")


    def output_a_set(self, first_enter=False) -> str:

        """
        complex set to string conversion function
        """

        line_set = ', '.join(self.elements)

        for subset in self.subsets:
            line_set += f', {subset.output_a_set()}' if self.elements else f'{subset.output_a_set()}'
        linse_result = '{%s}' % line_set  # if not first_enter else line_set
        return linse_result
