from typing import Dict

from model.validation import Validate


class Student:
    __dict_of_students: dict = {}
    __id: int = 0

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
            Validate.validate_data(new_student)
        except ValueError as e:
            cls.__id -= 1
            raise ValueError(e)
        cls.__dict_of_students[data['student_name']] = new_student

    @classmethod
    def get_all_students(cls):
        return cls.__dict_of_students

    # @classmethod
    # def get_dict_of_hours(cls)->Dict[str: int]:
    #     """Получить словарь суммы всех часов студентов"""
    #     dict_of_hours={i:j for i, j in cls.__dict_of_students.items()}


# new_student = {'student_name': 'Vlad', 'student_group': 121701, 'community_service': {1: 10, 2: 11, 3: 12, 4: 13}}
#
# Student.create_new_student(new_student)
#
# a: dict = Student.get_all_students()
#
# print(a['Vlad'].id)
