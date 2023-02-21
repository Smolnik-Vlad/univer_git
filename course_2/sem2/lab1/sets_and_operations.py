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

    def output_a_set(self, my_set: MySet, first_enter=False) -> str:

        """
        complex set to string conversion function
        """

        line_set = ', '.join(my_set.elements)

        for subset in my_set.subsets:
            line_set += f', {self.output_a_set(subset)}' if my_set.elements else f'{self.output_a_set(subset)}'
        linse_result = '{%s}' % line_set  # if not first_enter else line_set
        return linse_result

    def __find_suboperation(self, substr: str) -> int:
        check = 0
        for i in range(len(substr)):
            if substr[i] == "(":
                check += 1
            elif substr[i] == ")":
                check -= 1

            if check == 0:
                return i

    def __from_expression_to_list(self, expression: str) -> List[str]:
        sets_and_operations = list()
        line_set = expression.replace(' ', '')
        numb_of_element = 0
        first_position = 0
        last_position = 0
        # for i in range(len(line_set)):
        #     if line_set[i] in self.list_of_operations and i>first_position:
        #         class_set = self.__from_string_to_set(line_set[first_position+1:i-1])
        #         sets_and_operations.append(class_set)
        #         # else:
        #         #     class_set = self.solution(line_set[first_position + 1:i - 1])
        #         #     sets_and_operations.append(class_set)
        #
        #         sets_and_operations.append(line_set[i])
        #         first_position = i + 1
        #
        #
        #
        #     elif line_set[i] == "(" and i>=first_position:
        #         first_position = i
        #         last_position = self.__find_suboperation(line_set[first_position:])+i
        #         sets_and_operations.append(self.__from_expression_to_list(line_set[first_position+1:last_position]))
        #         if last_position+1 < len(line_set):
        #             sets_and_operations.append(line_set[last_position+1])
        #         first_position = last_position+1
        #
        #
        #
        #
        # if first_position < len(line_set):
        #     class_set = self.__from_string_to_set(line_set[first_position+2:-1])
        #     sets_and_operations.append(class_set)

        while numb_of_element < len(line_set):
            if line_set[numb_of_element] in self.list_of_operations:
                class_set = self.__from_string_to_set(line_set[first_position + 1:numb_of_element - 1])
                sets_and_operations.append(class_set)
                sets_and_operations.append(line_set[numb_of_element])
                first_position = numb_of_element + 1

            elif line_set[numb_of_element] == "(":
                last_position = self.__find_suboperation(line_set[first_position:]) + first_position
                sets_and_operations.append(self.__from_expression_to_list(line_set[first_position + 1:last_position]))
                if last_position + 1 < len(line_set):
                    sets_and_operations.append(line_set[last_position + 1])

                first_position = last_position + 2
                numb_of_element = last_position + 1

            numb_of_element += 1

        if first_position < len(line_set):
            class_set = self.__from_string_to_set(line_set[first_position + 1:-1])
            sets_and_operations.append(class_set)

        return sets_and_operations

    def solution(self, line_set: str):
        list_of_expression = self.__from_expression_to_list(line_set)
        return list_of_expression

    def check(self, s):
        # a = self.__from_string_to_set(s)
        # print(self.output_a_set(a, first_enter=True))
        self.solution(s)
