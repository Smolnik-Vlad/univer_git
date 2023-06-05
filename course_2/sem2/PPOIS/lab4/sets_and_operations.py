from typing import Dict, List

from set import MySet


class Sets_and_operations:
    list_of_operations = ['+', '*', '-', '/']

    @classmethod
    def __find_indexes(cls, s: str) -> Dict[int, int]:  # need to add try/except
        """
        to find the position of a subset in a string
        """

        bracket_positions = {}
        for i, c in enumerate(s):
            if c == '{' or c == '}':
                bracket_positions[i] = c

        left_bracket_positions = list()
        right_bracket_pos = list()
        opened = False
        counter = 0
        for i, c in bracket_positions.items():
            if c == '{':
                counter += 1
            elif c == '}':
                counter -= 1

            if not opened and counter == 1:
                left_bracket_positions.append(i + 1)
                opened = True
            elif opened and counter == 0:
                right_bracket_pos.append(i)
                opened = False

        subset_positions = dict(zip(left_bracket_positions, right_bracket_pos))

        return subset_positions

    def __from_string_to_set(self, line_set: str) -> MySet:

        """
        a function to represent a string as a set structure
        the outer set is passed without quotes
        """
        my_set = MySet()
        line_set = line_set.replace(' ', '')
        subsets_indexes = self.__find_indexes(line_set)
        subsets_str = list(map(lambda x: line_set[x[0]:x[1]], subsets_indexes.items()))
        # map(lambda x: my_set.subsets.append(cls.__create_set(subsets_str[x])), subsets_str)
        subsets = [self.__from_string_to_set(str_subset) for str_subset in subsets_str]
        my_set.subsets.extend(subsets)
        for i in subsets_str:
            line_set = line_set.replace(i, '')

        line_set = line_set.replace('{}', '')
        elements = list(filter(lambda a: a, line_set.split(',')))
        my_set.elements.extend(elements)

        return my_set

    def __find_suboperation(self, substr: str) -> int:
        check = 0
        for i in range(len(substr)):
            if substr[i] == "(":
                check += 1
            elif substr[i] == ")":
                check -= 1

            if check == 0:
                return i

    def from_expression_to_list(self, expression: str) -> List[str]:

        """
        The function is intended for translating an expression from a string into a list consisting of characters,
        sets and nested lists
        """

        sets_and_operations = list()
        line_set = expression.replace(' ', '')
        numb_of_element = 0
        first_position = 0
        last_position = 0

        while numb_of_element < len(line_set):
            if line_set[numb_of_element] in self.list_of_operations:
                class_set = self.__from_string_to_set(line_set[first_position + 1:numb_of_element - 1])
                sets_and_operations.append(class_set)
                sets_and_operations.append(line_set[numb_of_element])
                first_position = numb_of_element + 1

            elif line_set[numb_of_element] == "(":
                last_position = self.__find_suboperation(line_set[first_position:]) + first_position
                sets_and_operations.append(self.from_expression_to_list(line_set[first_position + 1:last_position]))
                if last_position + 1 < len(line_set):
                    sets_and_operations.append(line_set[last_position + 1])

                first_position = last_position + 2
                numb_of_element = last_position + 1

            numb_of_element += 1

        if first_position < len(line_set):
            class_set = self.__from_string_to_set(line_set[first_position + 1:-1])
            sets_and_operations.append(class_set)

        return sets_and_operations

    def __find_result(self, list_of_expression: list) -> MySet:
        while len(list_of_expression) > 1:
            if type(list_of_expression[0]) != list:
                first_set = list_of_expression.pop(0)
            else:
                first_set = self.__find_result(list_of_expression.pop(0))

            operation = list_of_expression.pop(0)

            if type(list_of_expression[0]) != list:
                second_set = list_of_expression.pop(0)
            else:
                second_set = self.__find_result(list_of_expression.pop(0))

            if operation == '+':
                list_of_expression.insert(0, first_set + second_set)
            elif operation == '*':
                list_of_expression.insert(0, first_set * second_set)
            elif operation == '-':
                list_of_expression.insert(0, first_set - second_set)
            elif operation == '/':
                list_of_expression.insert(0, first_set / second_set)

        if type(list_of_expression[0]) == list:
            return self.__find_result(list_of_expression[0])

        return list_of_expression.pop(0)

    def solution(self, line_set: str):
        if line_set.find('{') == -1:
            raise ValueError('The expression is given without brackets')

        list_of_expression = self.from_expression_to_list(line_set)
        result_set = self.__find_result(list_of_expression)
        return result_set

    @staticmethod
    def check(s):
        # a = self.__from_string_to_set(s)
        a = Sets_and_operations().solution(s)
        return a.output_a_set(first_enter=True)
