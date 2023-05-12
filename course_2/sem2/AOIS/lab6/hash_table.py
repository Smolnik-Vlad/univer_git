from typing import Optional, List


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, size_of_table=20):
        self.__size_of_table = size_of_table
        self.__table: List[List[Node]] = [None] * size_of_table

    def __get_hashed_key(self, key):
        if not key:
            raise ValueError('Key cant be empty')

        else:
            return sum([ord(key[i]) * 2 ** i for i in range(len(key))]) % self.__size_of_table

    def __hash_current_key(self, key):
        if type(key) == str:
            return self.__get_hashed_key(key)
        else:
            raise TypeError('key must be a string')

    def __setitem__(self, new_key: str, new_value: str):
        place_index: int = self.__hash_current_key(new_key)
        if self.__table[place_index]:
            for i in self.__table[place_index]:
                if i.key == new_key:
                    i.value = new_value
                    break
            else:
                new_element = Node(new_key, new_value)
                self.__table[place_index].append(new_element)

        else:
            new_element = Node(new_key, new_value)
            self.__table[place_index] = [new_element]

    def __getitem__(self, key):
        place_index = self.__hash_current_key(key)
        list_of_node = self.__table[place_index]
        if list_of_node:
            for node in list_of_node:
                if node.key == key:
                    return node
        else:
            raise KeyError("No such key")

    def __str__(self):
        str_of_elements = ''
        for i in range(len(self.__table)):
            str_of_elements += f'\n[{i}]: {self.__table[i]}'
        return str_of_elements

    def remove(self, key):
        place_index = self.__hash_current_key(key)
        if self.__table[place_index]:
            for node in self.__table[place_index]:
                if node.key == key:
                    self.__table[place_index].remove(node)
                    if not self.__table[place_index]:
                        self.__table[place_index] = None
                    break
        else:
            raise KeyError('No such key')


a = HashTable(25)
# a['hi'] = 'nigga'
# a['hi'] = 'fuck'
# a.remove('hi')