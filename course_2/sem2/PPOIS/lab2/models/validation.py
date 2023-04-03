from typing import List


class Validate:

    @staticmethod
    def spell_check(a: str):
        if not a.isalpha():
            raise ValueError("В ФИО присутствуют неверные символы")
        elif not a.istitle():
            raise ValueError("ФИО введено не с большой буквы")

    @staticmethod
    def check_community_service(service: str):
        if service == '':
            return "0"
        if not service.isdigit() and int(service) < 0:
            raise ValueError("Неправильное значение: должно быть целочисленное неотрицательное")
        return service

    @staticmethod
    def validate_student(new_element):
        check_name = new_element.student_name.split(" ")
        if len(check_name) > 3:
            raise ValueError("ФИО введено неверно!")

        for i in check_name:
            Validate.spell_check(i)  # вот тут проблема с проверкой на валидность имени

        if not new_element.student_group.isdigit():
            raise ValueError("Неверный номер группы")

        new_element.community_service = dict(enumerate(
            map(Validate.check_community_service, new_element.community_service.values())))

    @staticmethod
    def validate_filters(dict_of_filters: dict):
        student_name: str = dict_of_filters['student_name']
        low_limit: str = dict_of_filters['low_limit']
        high_limit: str = dict_of_filters['high_limit']

        if not student_name.replace(' ', '').isalpha():
            if student_name:
                raise ValueError('ФИО студента должно содержать только буквы!')

        if not high_limit.isdigit() and high_limit != '':
            raise ValueError('Верхний предел может быть только положительным целым числом')
        elif high_limit:
            if int(high_limit) < 0:
                raise ValueError('Число  верхнего предела должно быть положительным')

        if not low_limit.isdigit() and low_limit != '':
            raise ValueError('Нижний предел может быть только положительным целым числом')
        elif low_limit:
            if int(low_limit) < 0:
                raise ValueError('Число нижнего предела должно быть положительным')
