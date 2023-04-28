from constants import Constants
from set import MySet


class Another_operations(Constants):

    @staticmethod
    def size(my_set: MySet) -> int:
        return len(my_set.elements) + len(my_set.subsets)

    @staticmethod
    def psp(my_set: MySet) -> int:
        size: int = len(my_set.elements)
        for i in my_set.subsets:
            size += Another_operations.psp(i)
        return size

    @staticmethod
    def get_element(my_set: MySet, elem: int):
        return my_set[elem]

    def read_the_line_with_another_operatios(self,
                                             line: str):  # value - is a type of function, for example: A[0], value = '['
        if line.find('size') != -1:
            if line.find('['):
                raise Exception('Wrong format')
            self.read_the_lines(line[line.find('(') + 1:line.rfind(')')])
            return self.__class__.size(self.my_set)

        elif line.find('psp') != -1:
            if line.find('['):
                raise Exception('Wrong format')
            self.read_the_lines(line[line.find('(') + 1:line.rfind(')')])
            return self.__class__.psp(self.my_set)

        elif line.find('[') != -1:
            try:

                elem = int(line[line.find('[') + 1:line.rfind(']')])
                self.read_the_lines(line[:line.find('[')])

            except:
                raise Exception('Wrong format')
            else:
                try:
                    got_elem = self.__class__.get_element(self.my_set, elem)
                    print(got_elem.output_a_set(first_enter=True))
                    return got_elem


                except:
                    raise Exception('Out of range')
