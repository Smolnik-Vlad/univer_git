import xml
from xml.sax.handler import ContentHandler
import xml.etree.ElementTree as ET
from tkinter import filedialog

from models.models import Student


class XMLWriter:
    __file: str = ''

    @staticmethod
    def __writing_parser():
        all_students = Student.get_all_students_in_list()

        root = ET.Element("students")

        for student in all_students:
            element_student = ET.SubElement(root, 'student')
            element_id = ET.SubElement(element_student, 'id')
            element_id.text = student['id']
            element_name = ET.SubElement(element_student, 'name')
            element_name.text = student['name']
            element_group = ET.SubElement(element_student, 'group')
            element_group.text = student['group']

            element_community_services = []
            for i in range(10):
                element_community_services.append(ET.SubElement(element_student, f'community_service_{i}'))
            for i in range(10):
                element_community_services[i].text = student[f'community_service_{i}']

        tree = ET.ElementTree(root)
        return tree

    @classmethod
    def writer_as(cls):
        filename = filedialog.asksaveasfilename(defaultextension='.xml')
        if not filename:
            return  # пользователь не выбрал файл, просто выходим

        cls.__file = filename

        tree = XMLWriter.__writing_parser()

        tree.write(filename, encoding="utf-8", xml_declaration=True)

    @classmethod
    def writer(cls):
        if cls.__file:
            tree = XMLWriter.__writing_parser()
            tree.write(cls.__file, encoding="utf-8", xml_declaration=True)
        else:
            cls.writer_as()


