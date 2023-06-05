import random
from typing import List


class AccosiativeMemoryTable:
    def __init__(self, element_size):
        self.table_size = element_size  # Замените на желаемый размер памяти
        self.memory_table = [[0] * self.table_size for _ in range(self.table_size)]

    def __get_comparing_flags(self, reference_element, inspected_element):
        current_g, current_l = False, False
        for i in range(self.table_size):
            S_ji = bool(int(inspected_element[i]))
            a_i = bool(int(reference_element[i]))
            next_g = current_g or (not a_i and S_ji and not current_l)
            next_l = current_l or (a_i and not S_ji and not current_g)
            current_g, current_l = next_g, next_l
        return {'g_flag': current_g,
                'l_flag': current_l}

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
            filter(lambda x: self.__compare_2_elements(x, value) == 0, self.normal_table))

        if not below:
            suitable_elements.extend(list(
                filter(lambda x: self.__compare_2_elements(x, value) == 1, self.normal_table)))

        else:
            suitable_elements.extend((
                filter(lambda x: self.__compare_2_elements(x, value) == -1, self.normal_table)))

        suitable_elements = list(set(map(tuple, suitable_elements)))
        suitable_elements = list(map(list, suitable_elements))
        self.__selection_sort(suitable_elements) if below else self.__selection_sort(suitable_elements, reverse=True)
        print(suitable_elements)
        return suitable_elements[-1]

    def __compare_2_elements(self, comparable_object, reference):
        result_of_compare_elements = self.__get_comparing_flags(reference, comparable_object)
        if result_of_compare_elements['g_flag'] and not result_of_compare_elements['l_flag']:
            return 1
        elif not result_of_compare_elements['g_flag'] and result_of_compare_elements['l_flag']:
            return -1
        elif not result_of_compare_elements['g_flag'] and not result_of_compare_elements['l_flag']:
            return 0

    @staticmethod
    def __get_shifted_word(index, word):
        shift = (len(word) - index)
        a = word[:shift]
        b = word[shift:]

        shifted_word = b + a
        return shifted_word

    def create_new_entry(self, word, index: int):
        shifted_word = self.__get_shifted_word(index, word)
        for i in range(self.table_size):
            self.memory_table[i][index] = shifted_word[i]

    def __str__(self):
        table_print = ''
        for i in self.memory_table:
            table_print += f'{i}\n'
        return table_print

    @staticmethod
    def get_random_words(size):
        list_of_words = [[random.randint(0, 1) for _ in range(size)] for _ in range(size)]
        return list_of_words

    def get_choosen_word(self, number):
        try:
            shifted_word = list(map(lambda word: word[number], self.memory_table))
            word = shifted_word[number:] + shifted_word[:number]
            return word

        except:
            print("Could not be")

    def get_full_list_of_words(self):
        # В методе можно получаить нормальный список !
        list_of_words = [self.get_choosen_word(i) for i in range(self.table_size)]
        self.normal_table = list_of_words
        return list_of_words

    def f1(self, elemetns: List[list]):
        result = list(map(lambda x: 1 if x[0] and x[1] else 0, list(zip(elemetns[0], elemetns[1]))))
        return result

    def f14(self, elements: List[list]):
        result = self.f1(elements)
        result = [int(not x) for x in result]
        return result

    def f3(self, elements: List[list]):
        return elements[0]

    def f12(self, elements: List[list]):
        res = [int(not x) for x in elements[0]]
        return res

    def logical_function(self, func: str, elements: List[list]):
        operations = {'f1': self.f1,
                      'f14': self.f14,
                      'f3': self.f3,
                      'f12': self.f12}
        return operations[func](elements)

    def arithmetics(self, V: List[int]):
        results = list()
        list_of_all_words = self.get_full_list_of_words()
        suitable_words = list(filter(lambda x: x[:3] == V, list_of_all_words))
        for word in suitable_words:
            A, B = word[3:7], word[7:11]
            results.append(word[:11] + self.__sum_of_parts_of_words(A, B))

        results = dict(enumerate(results))
        return results

    def __sum_of_parts_of_words(self, word1, word2):

        el1 = [int(x) for x in word1]
        el2 = [int(x) for x in word2]
        result = ''
        carry = 0
        while len(el1) and len(el2):
            digital1 = el1.pop()
            digital2 = el2.pop()
            res = int(digital1 ^ digital2 ^ carry)
            result = str(res) + result
            carry = int((digital1 and digital2) or (digital1 ^ digital2) and carry)
        result = str(carry) + result
        return list(map(int, result))


if __name__ == '__main__':
    a = AccosiativeMemoryTable(16)
    list_of_words = AccosiativeMemoryTable.get_random_words(16)
    print(f'<Список слов: {list_of_words}>')
    for i in range(16):
        a.create_new_entry(list_of_words[i], i)
    print(a)

    print('________________________________________________________________')
    print(f'Выбранный элемент: {a.get_choosen_word(5)}')
    print(f'Целый элемент: {a.get_full_list_of_words()}')
    print(f'Наиближайший: {a.find_the_closest_value([0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0], below=False)}')

    print('logical functions')
    functions = ['f1', 'f14', 'f3', 'f12']
    print(f'f1: {a.logical_function(functions[0], [a.get_full_list_of_words()[0], a.get_full_list_of_words()[1]])}')
    print(f'f14: {a.logical_function(functions[1], [a.get_full_list_of_words()[0], a.get_full_list_of_words()[1]])}')
    print(f'f3: {a.logical_function(functions[2], [a.get_full_list_of_words()[0]])}')
    print(f'f12: {a.logical_function(functions[3], [a.get_full_list_of_words()[0]])}')

    print('sum')
    print(a.arithmetics([1, 0, 1]))
