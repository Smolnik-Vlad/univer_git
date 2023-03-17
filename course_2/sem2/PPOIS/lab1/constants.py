import json
from typing import Dict, List

from set import MySet
from sets_and_operations import Sets_and_operations
import csv


class Constants(Sets_and_operations):
    def __init__(self):
        self.const_MySet: Dict[str: set] = dict()
        self.const_list: List[str] = list()  # list of constants
        self.my_set: MySet = MySet()

    def __filter_consts_and_set(self, value: str):
        """
        special function for divide on consts and set
        """
        if value[0].istitle():
            if len(value) != 1:
                print(value)
                raise ValueError("Invalid variable name")
            self.const_list.append(value)

        else:
            self.read_the_lines(value)

    def __save_sets(self):
        data_from_file = dict()
        data = self.const_MySet
        try:
            with open('sets.json', 'r') as file:
                data_from_file.update(json.load(file))
        except FileNotFoundError:
            pass

        data_from_file.update(data)

        with open('sets.json', 'w') as file:
            json.dump(data_from_file, file)

    @classmethod
    def __get_sets(cls) -> Dict[str, dict]:
        try:
            with open('sets.json', 'r') as file:
                return json.load(file)

        except FileNotFoundError:
            return dict()

    def __create_const_MySet(self, string_for_parsing):
        string_for_parsing = string_for_parsing.replace(" ", "")
        last_eq = string_for_parsing.rfind("=")
        string_for_parsing = string_for_parsing[:last_eq+1] + '(' + string_for_parsing[last_eq+1:]+')'
        self.consts_and_values: List[str] = string_for_parsing.split("=")
        # map(self.__filter_consts_and_set, self.consts_and_values)
        for i in self.consts_and_values:
            self.__filter_consts_and_set(i)
        self.const_MySet = {const: self.my_set.from_class_to_list() for const in self.const_list}
        self.__save_sets()

    @classmethod
    def __get_saved_sets_str(cls, set_of_consts: list) -> dict:
        saved_sets: Dict[str, dict]  = {}
        try:
            saved_sets = cls.__get_sets()
        except:
            print('smthng wrong')
            raise ValueError('files format is wrong')

        for set in set_of_consts:
            if set not in saved_sets.keys():
                raise ValueError('Variable does not exist')
        selected_saved_sets: dict = {i: j for i, j in saved_sets.items() if i in set_of_consts}
        selectes_saved_sets_class = {i: MySet.from_set_to_class(j) for i, j in selected_saved_sets.items()}
        selected_saved_sets_str = {i: j.output_a_set(first_enter=True) for i, j in selectes_saved_sets_class.items()}           #вот здесь изменил вывод множества
        return selected_saved_sets_str

    def read_the_lines(self, strline: str):
        consts = []
        for i in strline:
            if i.isupper() and i not in consts:
                consts.append(i)

        saved_sets: dict = self.__get_saved_sets_str(consts)

        for i, j in saved_sets.items():
            strline = strline.replace(i, j)

        self.my_set = Sets_and_operations().solution(strline)

    def read_line(self, line: str):
        """
        function can define: do we use const for saving or not
        """
        if line.find('=') == -1:
            self.read_the_lines(line)
            print(self.my_set.output_a_set(first_enter=True))
            return self.my_set
        else:
            self.__create_const_MySet(line)

