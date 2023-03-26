from typing import Dict, List

from .validation import Validate
import tkinter.messagebox as mb


class Student:
    __id: int = 0
    list_of_groups: List[int] = ['none']
    __dict_of_students: dict = {}  # Dict['str': Student]
    __validated_filters: dict = {'student_name': '', 'student_group': 'none', 'low_limit': '', 'high_limit': ''}
    __dict_of_filtered_students: dict = {} # Dict['str': Student]
    __paginated_dict_of_filtered_students: Dict[int, dict] = {}
    __current_page: int = 1

    def __init__(self, data: dict, new_id: int):
        self.id = new_id
        self.student_name: str = data['student_name']
        self.student_group: str = (data['student_group'])
        self.community_service: Dict[int: int] = data['community_service']

    @classmethod
    def create_new_student(cls, data: dict):
        """Вызываем этот метод для добавления новой записи"""
        cls.__id += 1
        new_student = Student(data, cls.__id)
        if data['student_name'] in cls.__dict_of_students:
            raise ValueError("Студент с таким именем уже есть")
        try:
            Validate.validate_student(new_student)
        except ValueError as e:
            cls.__id -= 1
            raise ValueError(e)

        cls.__dict_of_students[data['student_name']] = new_student
        if new_student.student_group not in cls.list_of_groups:
            cls.list_of_groups.append(new_student.student_group)

    @classmethod
    def get_all_students(cls):
        return cls.__dict_of_students

    @classmethod
    def set_up_filters(cls, filters: dict):
        Validate.validate_filters(filters)
        # ['student_name', 'student_group', 'low_limit', 'high_limit']
        cls.__validated_filters = filters

    @classmethod
    def __selection_of_suitable_values_by_clock(cls, elem, low_high: bool):  # low_high == True -> high, else False
        list_of_hours = list(map(int, elem[1].community_service.values()))
        sum_of_hours: int = sum(list_of_hours)

        if low_high:
            if cls.__validated_filters['high_limit'] == '':
                return True
            return sum_of_hours <= int(cls.__validated_filters['high_limit'])
        else:
            if cls.__validated_filters['low_limit'] == '':
                return True
            return sum_of_hours >= int(cls.__validated_filters['low_limit'])

    @classmethod
    def __select_of_suitable_values_by_name(cls, entry):
        return cls.__validated_filters['student_name'] in entry[0]

    @classmethod
    def __select_of_suitable_values_by_group(cls, entry):
        if cls.__validated_filters['student_group'] == 'none':
            return True
        else:
            return True if int(cls.__validated_filters['student_group']) == int(entry[1].student_group) else False

    @classmethod
    def get_filtered_students(cls):
        """Функция, которая фильтрует всех студентов по заданным параметрам"""
        cls.__dict_of_filtered_students = dict(
            filter(cls.__select_of_suitable_values_by_name, cls.__dict_of_students.items()))

        cls.__dict_of_filtered_students = dict(
            filter(cls.__select_of_suitable_values_by_group, cls.__dict_of_filtered_students.items()))

        cls.__dict_of_filtered_students = dict(
            filter(lambda x: Student.__selection_of_suitable_values_by_clock(x, False),
                   cls.__dict_of_filtered_students.items()))

        cls.__dict_of_filtered_students = dict(filter(
            lambda x: Student.__selection_of_suitable_values_by_clock(x, True),
            cls.__dict_of_filtered_students.items()))

        return cls.__dict_of_filtered_students

    @classmethod
    def __get_paginated_filtered_students(cls, items_per_page: int = 5) -> Dict[int, Dict]:
        cls.__paginated_dict_of_filtered_students = {}

        num_pages = len(cls.__dict_of_filtered_students) // items_per_page + 1 if len(
            cls.__dict_of_filtered_students) % 5 != 0 else len(cls.__dict_of_filtered_students) // items_per_page

        for i in range(num_pages):
            page = {}
            for j, (key, value) in enumerate(cls.__dict_of_filtered_students.items()):
                if i * items_per_page <= j < (i + 1) * items_per_page:
                    page[key] = value
            cls.__paginated_dict_of_filtered_students[i + 1] = page

    @classmethod
    def get_pages_of_filtered_students(cls):
        cls.get_filtered_students()
        cls.__get_paginated_filtered_students()

        # просто проверка на наличие записи
        if cls.__paginated_dict_of_filtered_students:
            cls.__current_page = 1
            return cls.__paginated_dict_of_filtered_students[1]
        else:
            return False

    @classmethod
    def __check_paginated_dict(cls):
        if cls.__paginated_dict_of_filtered_students and cls.__paginated_dict_of_filtered_students[1]:
            return True
        elif cls.__paginated_dict_of_filtered_students:
            mb.showinfo("Инфо", "Ни одной записи не было создано!")
            return False

        else:
            mb.showinfo("Инфо", "Ни одной записи не было создано!")
            cls.get_pages_of_filtered_students()

    @classmethod
    def get_first_page(cls):
        if cls.__check_paginated_dict():
            if cls.__current_page != 1:
                cls.__current_page = 1
                return cls.__paginated_dict_of_filtered_students[1]
            else:
                mb.showinfo("Инфо", "Это и так первая страница")
                return cls.__paginated_dict_of_filtered_students[1]

        else:
            # return cls.__paginated_dict_of_filtered_students[1]
            return False

    @classmethod
    def get_previous_page(cls):
        if cls.__check_paginated_dict():

            if cls.__current_page > 1:
                cls.__current_page -= 1
                return cls.__paginated_dict_of_filtered_students[cls.__current_page]
            else:
                mb.showinfo("Инфо", "Это и так первая страница")
                return cls.__paginated_dict_of_filtered_students[1]
        else:
            # return cls.__paginated_dict_of_filtered_students[1]
            return False

    @classmethod
    def get_last_page(cls):
        if cls.__check_paginated_dict():

            if cls.__current_page + 1 <= len(cls.__paginated_dict_of_filtered_students):
                cls.__current_page = list(cls.__paginated_dict_of_filtered_students.keys())[-1]
                return cls.__paginated_dict_of_filtered_students[cls.__current_page]
            else:
                mb.showinfo("Инфо", "Это и так последняя страница")
                return cls.__paginated_dict_of_filtered_students[len(cls.__paginated_dict_of_filtered_students)]
        else:
            return False
            # return cls.__paginated_dict_of_filtered_students[1]

    @classmethod
    def get_next_page(cls):
        if cls.__check_paginated_dict():
            if cls.__current_page + 1 <= len(cls.__paginated_dict_of_filtered_students):
                cls.__current_page += 1
                return cls.__paginated_dict_of_filtered_students[cls.__current_page]

            else:
                mb.showinfo("Инфо", "Это и так последняя страница")
                return cls.__paginated_dict_of_filtered_students[len(cls.__paginated_dict_of_filtered_students)]

        else:
            return False
            # return cls.__paginated_dict_of_filtered_students[1]

    @classmethod
    def get_numbers_of_pages(cls):
        return cls.__current_page, len(cls.__paginated_dict_of_filtered_students)

    @classmethod
    def set_default_filters(cls):
        cls.__validated_filters = {'student_name': '', 'student_group': 'none', 'low_limit': '', 'high_limit': ''}

    @classmethod
    def delete_students(cls, name_of_student: str = False):
        deleted_students = []
        if name_of_student:
            cls.__dict_of_students.pop(name_of_student)
            deleted_students.append(name_of_student)

        else:
            for student in cls.__dict_of_filtered_students.keys():
                cls.__dict_of_students.pop(student)
                deleted_students.append(student)
        mb.showinfo("Удаленные студенты", f"Имена удаленных студентов: {', '.join(deleted_students)}")
