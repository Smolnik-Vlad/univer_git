import random
from typing import List


class Processor:
    def __init__(self, size_of_element: int, table_size: int):
        self.__element_size = size_of_element
        self.__table_of_elements = []
        self.__table_size = table_size
        self.__fill_table()

    def __get_comparing_flags(self, reference_element, inspected_element):
        current_g, current_l = False, False
        for i in range(self.__element_size):
            S_ji = bool(int(inspected_element[i]))
            a_i = bool(int(reference_element[i]))
            next_g = current_g or (not a_i and S_ji and not current_l)
            next_l = current_l or (a_i and not S_ji and not current_g)
            current_g, current_l = next_g, next_l
        return {'g_flag': current_g,
                'l_flag': current_l}

    def __compare_2_elements(self, comparable_object, reference):
        result_of_compare_elements = self.__get_comparing_flags(reference, comparable_object)
        if result_of_compare_elements['g_flag'] and not result_of_compare_elements['l_flag']:
            return 1
        elif not result_of_compare_elements['g_flag'] and result_of_compare_elements['l_flag']:
            return -1
        elif not result_of_compare_elements['g_flag'] and not result_of_compare_elements['l_flag']:
            return 0

    # def __sort_elements(self, list_of_elements: List[list], reverse=False):
    #     size = len(list_of_elements)
    #     for i in range(size - 1):
    #         for j in range(size - i - 1):
    #             flag = -1 if not reverse else 1
    #             if self.__compare_2_elements(list_of_elements[j], list_of_elements[j + 1]) == flag:
    #                 list_of_elements[j], list_of_elements[j + 1] = list_of_elements[j + 1], list_of_elements[j]

    def __selection_sort(self, list_of_elements: List[list], reverse=False):
        size = len(list_of_elements)
        for i in range(size - 1):
            min_index = i
            for j in range(i + 1, size):
                flag = -1 if not reverse else 1
                # if list_of_elements[j] < list_of_elements[min_index]:
                if self.__compare_2_elements(list_of_elements[j], list_of_elements[min_index]) == flag:
                    min_index = j
            list_of_elements[i], list_of_elements[min_index] = list_of_elements[min_index], list_of_elements[i]
        return list_of_elements

    def find_the_closest_value(self, value: List[int], below=True):
        """Здесь считается самое близкое значение, передается близкое значение и below = True - снизу, False - сверху"""
        suitable_elements = list(
            filter(lambda x: self.__compare_2_elements(x, value) == 0, self.__table_of_elements))

        if not below:
            suitable_elements.extend(list(
                filter(lambda x: self.__compare_2_elements(x, value) == 1, self.__table_of_elements)))

        else:
            suitable_elements.extend((
                filter(lambda x: self.__compare_2_elements(x, value) == -1, self.__table_of_elements)))

        suitable_elements = list(set(map(tuple, suitable_elements)))
        suitable_elements = list(map(list, suitable_elements))
        self.__selection_sort(suitable_elements) if below else self.__selection_sort(suitable_elements, reverse=True)
        print(suitable_elements)
        return suitable_elements[-1]

    def get_sort_list(self, reverse=False):
        return self.__selection_sort(self.__table_of_elements[:], reverse=reverse)

    def __fill_table(self):
        for i in range(self.__table_size):
            self.__table_of_elements.append([random.randint(0, 1) for _ in range(self.__element_size)])

    def __str__(self):
        table_str = 'Memory table: \n'
        for element in self.__table_of_elements:
            new_element = ''.join(list(map(lambda a: str(a), element)))
            table_str += new_element
            table_str += '\n'
        return table_str
