from typing import List


class Validate:

    @staticmethod
    def spell_check(a: str):
        if not a.isalpha():
            raise ValueError("В ФИО присутствуют неверные символы")

    @staticmethod
    def check_community_service(service: str):
        if service == '':
            return 0
        if not service.isdigit():
            raise ValueError("Неправильное значение айайай")
        return service

    @staticmethod
    def validate_data(new_element):
        check_name = new_element.student_name.split(" ")
        if len(check_name) > 3:
            raise ValueError("ФИО введено неверно!")

        for i in check_name:
            Validate.spell_check(i)  # вот тут проблема с проверкой на валидность имени

        if not new_element.student_group.isdigit():
            raise ValueError("Неверный номер группы")

        new_element.community_service = dict(enumerate(
            map(Validate.check_community_service, new_element.community_service.values())))
